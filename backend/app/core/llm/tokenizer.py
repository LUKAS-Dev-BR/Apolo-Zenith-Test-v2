import os
import json
import pickle
from typing import List, Optional
from pathlib import Path

class SentencePieceTokenizer:
    def __init__(self, vocab_size: int = 32000):
        self.vocab_size = vocab_size
        self.vocab = {}
        self.inverse_vocab = {}
        self.merges = []
        self.special_tokens = {
            "<pad>": 0,
            "<unk>": 1,
            "<bos>": 2,
            "<eos>": 3,
            "<sep>": 4,
            "<cls>": 5,
            "<mask>": 6,
            "<user>": 7,
            "<assistant>": 8
        }
        
    def train(self, corpus: List[str]):
        word_freqs = {}
        for text in corpus:
            words = text.split()
            for word in words:
                chars = list(word) + ["</w>"]
                word_freqs[tuple(chars)] = word_freqs.get(tuple(chars), 0) + 1
        
        char_freqs = {}
        for word, freq in word_freqs.items():
            for i in range(len(word) - 1):
                pair = (word[i], word[i + 1])
                char_freqs[pair] = char_freqs.get(pair, 0) + freq
        
        for i in range(self.vocab_size - len(self.special_tokens)):
            if not char_freqs:
                break
            
            best_pair = max(char_freqs, key=char_freqs.get)
            self.merges.append(best_pair)
            
            new_word = best_pair[0] + best_pair[1]
            new_word_freqs = {}
            
            for word, freq in word_freqs.items():
                new_word_list = []
                j = 0
                while j < len(word):
                    if j < len(word) - 1 and word[j] == best_pair[0] and word[j + 1] == best_pair[1]:
                        new_word_list.append(new_word)
                        j += 2
                    else:
                        new_word_list.append(word[j])
                        j += 1
                new_word_freqs[tuple(new_word_list)] = freq
            
            word_freqs = new_word_freqs
            
            char_freqs = {}
            for word, freq in word_freqs.items():
                for j in range(len(word) - 1):
                    pair = (word[j], word[j + 1])
                    char_freqs[pair] = char_freqs.get(pair, 0) + freq
        
        vocab_idx = len(self.special_tokens)
        for token in self.special_tokens:
            self.vocab[token] = self.special_tokens[token]
            self.inverse_vocab[self.special_tokens[token]] = token
        
        all_chars = set()
        for word in word_freqs:
            for char in word:
                all_chars.add(char)
        
        for char in sorted(all_chars):
            if vocab_idx >= self.vocab_size:
                break
            if char not in self.vocab:
                self.vocab[char] = vocab_idx
                self.inverse_vocab[vocab_idx] = char
                vocab_idx += 1
        
        for word in word_freqs:
            if vocab_idx >= self.vocab_size:
                break
            word_str = "".join(word)
            if word_str not in self.vocab:
                self.vocab[word_str] = vocab_idx
                self.inverse_vocab[vocab_idx] = word_str
                vocab_idx += 1
    
    def encode(self, text: str) -> List[int]:
        tokens = []
        words = text.split()
        
        for word in words:
            chars = list(word) + ["</w>"]
            
            for merge in self.merges:
                i = 0
                while i < len(chars) - 1:
                    if chars[i] == merge[0] and chars[i + 1] == merge[1]:
                        chars = chars[:i] + [merge[0] + merge[1]] + chars[i + 2:]
                    else:
                        i += 1
            
            for char in chars:
                if char in self.vocab:
                    tokens.append(self.vocab[char])
                else:
                    tokens.append(self.special_tokens["<unk>"])
        
        return [self.special_tokens["<bos>"]] + tokens + [self.special_tokens["<eos>"]]
    
    def decode(self, ids: List[int]) -> str:
        tokens = []
        for idx in ids:
            if idx in self.inverse_vocab:
                token = self.inverse_vocab[idx]
                if token == "</w>":
                    tokens.append(" ")
                elif token not in self.special_tokens:
                    tokens.append(token)
        
        return "".join(tokens).strip()
    
    def save(self, path: str):
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, 'wb') as f:
            pickle.dump({
                'vocab': self.vocab,
                'inverse_vocab': self.inverse_vocab,
                'merges': self.merges,
                'special_tokens': self.special_tokens,
                'vocab_size': self.vocab_size
            }, f)
    
    def load(self, path: str):
        with open(path, 'rb') as f:
            data = pickle.load(f)
            self.vocab = data['vocab']
            self.inverse_vocab = data['inverse_vocab']
            self.merges = data['merges']
            self.special_tokens = data['special_tokens']
            self.vocab_size = data['vocab_size']
