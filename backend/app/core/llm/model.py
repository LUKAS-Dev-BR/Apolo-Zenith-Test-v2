import torch
import torch.nn as nn
import math
from typing import Optional, Tuple
from app.core.llm.attention import CausalSelfAttention, MultiHeadAttention
from app.core.llm.tokenizer import SentencePieceTokenizer
from app.config import settings

class RMSNorm(nn.Module):
    def __init__(self, d_model: int, eps: float = 1e-6):
        super().__init__()
        self.weight = nn.Parameter(torch.ones(d_model))
        self.eps = eps
        
    def forward(self, x):
        norm = torch.rsqrt(x.pow(2).mean(-1, keepdim=True) + self.eps)
        return x * norm * self.weight

class SwiGLU(nn.Module):
    def __init__(self, d_model: int, d_ff: int):
        super().__init__()
        self.w1 = nn.Linear(d_model, d_ff, bias=False)
        self.w2 = nn.Linear(d_ff, d_model, bias=False)
        self.w3 = nn.Linear(d_model, d_ff, bias=False)
        
    def forward(self, x):
        return self.w2(nn.functional.silu(self.w1(x)) * self.w3(x))

class TransformerBlock(nn.Module):
    def __init__(self, d_model: int, n_heads: int, d_ff: int, dropout: float = 0.1):
        super().__init__()
        self.attention = CausalSelfAttention(d_model, n_heads, dropout)
        self.feed_forward = SwiGLU(d_model, d_ff)
        self.norm1 = RMSNorm(d_model)
        self.norm2 = RMSNorm(d_model)
        self.dropout = nn.Dropout(dropout)
        
    def forward(self, x, mask=None):
        x = x + self.dropout(self.attention(self.norm1(x), mask))
        x = x + self.dropout(self.feed_forward(self.norm2(x)))
        return x

class RoPE(nn.Module):
    def __init__(self, d_model: int, max_seq_len: int = 100096):
        super().__init__()
        self.d_model = d_model
        self.max_seq_len = max_seq_len
        
        freqs = 1.0 / (10000 ** (torch.arange(0, d_model, 2).float() / d_model))
        self.register_buffer('freqs', freqs)
        
    def forward(self, x, seq_len):
        t = torch.arange(seq_len, device=x.device).float()
        freqs = torch.outer(t, self.freqs)
        cos = freqs.cos().unsqueeze(0)
        sin = freqs.sin().unsqueeze(0)
        
        x1 = x[..., ::2]
        x2 = x[..., 1::2]
        
        rotated = torch.stack([-x2, x1], dim=-1).flatten(-2)
        
        return x * cos + rotated * sin

class ApoloLLM(nn.Module):
    def __init__(self, config: dict = None):
        super().__init__()
        
        if config is None:
            config = settings.LLM_CONFIG
            
        self.config = config
        self.vocab_size = config['vocab_size']
        self.d_model = config['d_model']
        self.n_heads = config['n_heads']
        self.n_layers = config['n_layers']
        self.d_ff = config['d_ff']
        self.max_seq_len = config['max_seq_len']
        self.dropout = config['dropout']
        
        self.token_embedding = nn.Embedding(self.vocab_size, self.d_model)
        self.rope = RoPE(self.d_model, self.max_seq_len)
        
        self.layers = nn.ModuleList([
            TransformerBlock(self.d_model, self.n_heads, self.d_ff, self.dropout)
            for _ in range(self.n_layers)
        ])
        
        self.norm = RMSNorm(self.d_model)
        self.output_head = nn.Linear(self.d_model, self.vocab_size, bias=False)
        
        self.token_embedding.weight = self.output_head.weight
        
        self.tokenizer = SentencePieceTokenizer(self.vocab_size)
        
        self._init_weights()
        
    def _init_weights(self):
        for module in self.modules():
            if isinstance(module, nn.Linear):
                torch.nn.init.normal_(module.weight, mean=0.0, std=0.02)
                if module.bias is not None:
                    torch.nn.init.zeros_(module.bias)
            elif isinstance(module, nn.Embedding):
                torch.nn.init.normal_(module.weight, mean=0.0, std=0.02)
    
    def forward(self, input_ids: torch.Tensor, targets: Optional[torch.Tensor] = None):
        batch_size, seq_len = input_ids.shape
        
        x = self.token_embedding(input_ids)
        x = self.rope(x, seq_len)
        
        causal_mask = torch.triu(torch.ones(seq_len, seq_len, device=x.device), diagonal=1).bool()
        
        for layer in self.layers:
            x = layer(x, ~causal_mask)
        
        x = self.norm(x)
        logits = self.output_head(x)
        
        loss = None
        if targets is not None:
            shift_logits = logits[..., :-1, :].contiguous()
            shift_labels = targets[..., 1:].contiguous()
            loss = nn.functional.cross_entropy(
                shift_logits.view(-1, self.vocab_size),
                shift_labels.view(-1),
                ignore_index=0
            )
        
        return logits, loss
    
    @torch.no_grad()
    def generate(self, prompt: str, reasoning_mode: str = "normal", max_new_tokens: int = 1024):
        from app.config import settings
        
        mode_config = settings.REASONING_MODES.get(reasoning_mode, settings.REASONING_MODES["normal"])
        
        input_ids = self.tokenizer.encode(prompt)
        input_tensor = torch.tensor([input_ids], dtype=torch.long)
        
        generated = input_ids.copy()
        
        for _ in range(min(max_new_tokens, mode_config["tokens"])):
            logits, _ = self.forward(input_tensor)
            next_token_logits = logits[:, -1, :] / 0.7
            
            probs = torch.softmax(next_token_logits, dim=-1)
            next_token = torch.argmax(probs, dim=-1)
            
            if next_token.item() == self.tokenizer.special_tokens["<eos>"]:
                break
            
            generated.append(next_token.item())
            input_tensor = torch.tensor([generated], dtype=torch.long)
        
        return self.tokenizer.decode(generated)
    
    def save_checkpoint(self, path: str, optimizer=None, epoch: int = 0):
        checkpoint = {
            'model_state_dict': self.state_dict(),
            'config': self.config,
            'epoch': epoch
        }
        if optimizer is not None:
            checkpoint['optimizer_state_dict'] = optimizer.state_dict()
        
        torch.save(checkpoint, path)
    
    def load_checkpoint(self, path: str):
        checkpoint = torch.load(path, map_location='cpu')
        self.load_state_dict(checkpoint['model_state_dict'])
        return checkpoint.get('epoch', 0)
