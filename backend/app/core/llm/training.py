import torch
import torch.nn as nn
from torch.utils.data import Dataset, DataLoader
from typing import List, Tuple, Optional
import os
import json
from pathlib import Path

from app.core.llm.model import ApoloLLM
from app.config import settings

class TextDataset(Dataset):
    def __init__(self, texts: List[str], tokenizer, max_length: int = 2048):
        self.texts = texts
        self.tokenizer = tokenizer
        self.max_length = max_length
        
    def __len__(self):
        return len(self.texts)
    
    def __getitem__(self, idx):
        text = self.texts[idx]
        tokens = self.tokenizer.encode(text)
        
        if len(tokens) > self.max_length:
            tokens = tokens[:self.max_length]
        else:
            tokens = tokens + [0] * (self.max_length - len(tokens))
        
        return torch.tensor(tokens, dtype=torch.long)

class LLMTrainer:
    def __init__(self, model: ApoloLLM, device: str = "cpu"):
        self.model = model.to(device)
        self.device = device
        self.optimizer = torch.optim.AdamW(
            model.parameters(),
            lr=1e-4,
            weight_decay=0.01,
            betas=(0.9, 0.95)
        )
        self.scaler = torch.cuda.amp.GradScaler() if device == "cuda" else None
        
    def train_epoch(self, dataloader: DataLoader, epoch: int, accumulation_steps: int = 4):
        self.model.train()
        total_loss = 0
        
        self.optimizer.zero_grad()
        
        for batch_idx, batch in enumerate(dataloader):
            batch = batch.to(self.device)
            
            with torch.cuda.amp.autocast(enabled=self.scaler is not None):
                logits, loss = self.model(batch, batch)
                loss = loss / accumulation_steps
            
            if self.scaler is not None:
                self.scaler.scale(loss).backward()
            else:
                loss.backward()
            
            if (batch_idx + 1) % accumulation_steps == 0:
                if self.scaler is not None:
                    self.scaler.unscale_(self.optimizer)
                    torch.nn.utils.clip_grad_norm_(self.model.parameters(), 1.0)
                    self.scaler.step(self.optimizer)
                    self.scaler.update()
                else:
                    torch.nn.utils.clip_grad_norm_(self.model.parameters(), 1.0)
                    self.optimizer.step()
                
                self.optimizer.zero_grad()
            
            total_loss += loss.item() * accumulation_steps
            
            if batch_idx % 100 == 0:
                print(f"Epoch {epoch}, Batch {batch_idx}, Loss: {loss.item() * accumulation_steps:.4f}")
        
        return total_loss / len(dataloader)
    
    def pretrain(self, texts: List[str], epochs: int = 10, batch_size: int = 4):
        print("Iniciando pré-treinamento...")
        
        dataset = TextDataset(texts, self.model.tokenizer)
        dataloader = DataLoader(dataset, batch_size=batch_size, shuffle=True)
        
        for epoch in range(epochs):
            avg_loss = self.train_epoch(dataloader, epoch)
            print(f"Epoch {epoch + 1}/{epochs} - Avg Loss: {avg_loss:.4f}")
            
            checkpoint_dir = settings.CHECKPOINTS_DIR
            checkpoint_dir.mkdir(exist_ok=True)
            self.model.save_checkpoint(
                str(checkpoint_dir / f"pretrain_epoch_{epoch + 1}.pt"),
                self.optimizer,
                epoch
            )
        
        print("Pré-treinamento concluído!")
    
    def sft(self, conversations: List[List[dict]], epochs: int = 5, batch_size: int = 2):
        print("Iniciando Supervised Fine-Tuning (SFT)...")
        
        sft_texts = []
        for conv in conversations:
            text = ""
            for turn in conv:
                if turn["role"] == "user":
                    text += f"<user> {turn['content']} "
                elif turn["role"] == "assistant":
                    text += f"<assistant> {turn['content']} "
            text += "<eos>"
            sft_texts.append(text)
        
        dataset = TextDataset(sft_texts, self.model.tokenizer)
        dataloader = DataLoader(dataset, batch_size=batch_size, shuffle=True)
        
        for epoch in range(epochs):
            avg_loss = self.train_epoch(dataloader, epoch)
            print(f"SFT Epoch {epoch + 1}/{epochs} - Avg Loss: {avg_loss:.4f}")
            
            checkpoint_dir = settings.CHECKPOINTS_DIR
            checkpoint_dir.mkdir(exist_ok=True)
            self.model.save_checkpoint(
                str(checkpoint_dir / f"sft_epoch_{epoch + 1}.pt"),
                self.optimizer,
                epoch
            )
        
        print("SFT concluído!")
