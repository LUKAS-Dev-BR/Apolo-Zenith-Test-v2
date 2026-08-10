import torch
import torch.nn as nn
import torch.nn.functional as F
from typing import Tuple, Optional
from app.core.multimodal.diffusion import GaussianDiffusion

class ResBlock(nn.Module):
    def __init__(self, in_channels: int, out_channels: int, time_emb_dim: int):
        super().__init__()
        self.norm1 = nn.GroupNorm(32, in_channels)
        self.conv1 = nn.Conv2d(in_channels, out_channels, 3, padding=1)
        self.norm2 = nn.GroupNorm(32, out_channels)
        self.conv2 = nn.Conv2d(out_channels, out_channels, 3, padding=1)
        
        self.time_mlp = nn.Sequential(
            nn.SiLU(),
            nn.Linear(time_emb_dim, out_channels)
        )
        
        self.residual_conv = nn.Conv2d(in_channels, out_channels, 1) if in_channels != out_channels else nn.Identity()
        
    def forward(self, x: torch.Tensor, time_emb: torch.Tensor) -> torch.Tensor:
        h = self.norm1(x)
        h = F.silu(h)
        h = self.conv1(h)
        
        time_emb = self.time_mlp(time_emb).unsqueeze(-1).unsqueeze(-1)
        h = h + time_emb
        
        h = self.norm2(h)
        h = F.silu(h)
        h = self.conv2(h)
        
        return h + self.residual_conv(x)

class CrossAttention2D(nn.Module):
    def __init__(self, channels: int, context_dim: int, num_heads: int = 8):
        super().__init__()
        self.num_heads = num_heads
        self.head_dim = channels // num_heads
        
        self.norm = nn.GroupNorm(32, channels)
        self.q = nn.Conv2d(channels, channels, 1)
        self.k = nn.Linear(context_dim, channels)
        self.v = nn.Linear(context_dim, channels)
        self.out = nn.Conv2d(channels, channels, 1)
        
    def forward(self, x: torch.Tensor, context: torch.Tensor) -> torch.Tensor:
        batch_size, channels, height, width = x.shape
        
        h = self.norm(x)
        q = self.q(h).view(batch_size, self.num_heads, self.head_dim, height * width)
        q = q.permute(0, 1, 3, 2)
        
        k = self.k(context).view(batch_size, -1, self.num_heads, self.head_dim).permute(0, 2, 1, 3)
        v = self.v(context).view(batch_size, -1, self.num_heads, self.head_dim).permute(0, 2, 1, 3)
        
        attn = torch.matmul(q, k.transpose(-2, -1)) / (self.head_dim ** 0.5)
        attn = F.softmax(attn, dim=-1)
        
        out = torch.matmul(attn, v)
        out = out.permute(0, 1, 3, 2).view(batch_size, channels, height, width)
        out = self.out(out)
        
        return x + out

class UNet2D(nn.Module):
    def __init__(self, in_channels: int = 3, base_channels: int = 128, channel_mults: Tuple = (1, 2, 4, 8), time_emb_dim: int = 512, context_dim: int = 768):
        super().__init__()
        
        self.time_mlp = nn.Sequential(
            nn.Linear(128, time_emb_dim),
            nn.SiLU(),
            nn.Linear(time_emb_dim, time_emb_dim)
        )
        
        self.input_conv = nn.Conv2d(in_channels, base_channels, 3, padding=1)
        
        self.down_blocks = nn.ModuleList()
        self.down_samples = nn.ModuleList()
        
        channels = [base_channels]
        curr_channels = base_channels
        
        for mult in channel_mults:
            out_channels = base_channels * mult
            self.down_blocks.append(nn.ModuleList([
                ResBlock(curr_channels, out_channels, time_emb_dim),
                CrossAttention2D(out_channels, context_dim),
                ResBlock(out_channels, out_channels, time_emb_dim)
            ]))
            channels.append(out_channels)
            curr_channels = out_channels
            self.down_samples.append(nn.Conv2d(out_channels, out_channels, 3, stride=2, padding=1))
        
        self.mid_block1 = ResBlock(curr_channels, curr_channels, time_emb_dim)
        self.mid_attn = CrossAttention2D(curr_channels, context_dim)
        self.mid_block2 = ResBlock(curr_channels, curr_channels, time_emb_dim)
        
        self.up_blocks = nn.ModuleList()
        self.up_samples = nn.ModuleList()
        
        for mult in reversed(channel_mults):
            out_channels = base_channels * mult
            self.up_blocks.append(nn.ModuleList([
                ResBlock(curr_channels + channels.pop(), out_channels, time_emb_dim),
                CrossAttention2D(out_channels, context_dim),
                ResBlock(out_channels, out_channels, time_emb_dim)
            ]))
            self.up_samples.append(nn.ConvTranspose2d(out_channels, out_channels, 4, stride=2, padding=1))
            curr_channels = out_channels
        
        self.output_norm = nn.GroupNorm(32, curr_channels)
        self.output_conv = nn.Conv2d(curr_channels, in_channels, 3, padding=1)
        
    def forward(self, x: torch.Tensor, t: torch.Tensor, context: Optional[torch.Tensor] = None) -> torch.Tensor:
        batch_size = x.shape[0]
        
        t_emb = torch.randn(batch_size, 128, device=x.device)
        t_emb = self.time_mlp(t_emb)
        
        h = self.input_conv(x)
        
        residuals = [h]
        
        for block, attn, block2 in self.down_blocks:
            h = block(h, t_emb)
            if context is not None:
                h = attn(h, context)
            h = block2(h, t_emb)
            residuals.append(h)
            h = self.down_samples[self.down_blocks.index((block, attn, block2))](h)
        
        h = self.mid_block1(h, t_emb)
        if context is not None:
            h = self.mid_attn(h, context)
        h = self.mid_block2(h, t_emb)
        
        for i, (block, attn, block2) in enumerate(self.up_blocks):
            h = self.up_samples[i](h)
            h = torch.cat([h, residuals.pop()], dim=1)
            h = block(h, t_emb)
            if context is not None:
                h = attn(h, context)
            h = block2(h, t_emb)
        
        h = self.output_norm(h)
        h = F.silu(h)
        h = self.output_conv(h)
        
        return h

class CLIPTextEncoder(nn.Module):
    def __init__(self, vocab_size: int = 32000, d_model: int = 768, n_heads: int = 12, n_layers: int = 12, max_seq_len: int = 77):
        super().__init__()
        
        self.token_embedding = nn.Embedding(vocab_size, d_model)
        self.position_embedding = nn.Embedding(max_seq_len, d_model)
        
        encoder_layer = nn.TransformerEncoderLayer(
            d_model=d_model,
            nhead=n_heads,
            dim_feedforward=d_model * 4,
            batch_first=True
        )
        self.transformer = nn.TransformerEncoder(encoder_layer, num_layers=n_layers)
        
        self.norm = nn.LayerNorm(d_model)
        
    def forward(self, input_ids: torch.Tensor) -> torch.Tensor:
        seq_len = input_ids.shape[1]
        positions = torch.arange(seq_len, device=input_ids.device).unsqueeze(0)
        
        x = self.token_embedding(input_ids) + self.position_embedding(positions)
        
        mask = torch.triu(torch.ones(seq_len, seq_len, device=input_ids.device), diagonal=1).bool()
        
        x = self.transformer(x, mask=mask)
        x = self.norm(x)
        
        return x

class TextToImagePipeline(nn.Module):
    def __init__(self, vocab_size: int = 32000, d_model: int = 768):
        super().__init__()
        
        self.text_encoder = CLIPTextEncoder(vocab_size, d_model)
        self.unet = UNet2D(in_channels=4, base_channels=128, context_dim=d_model)
        self.diffusion = GaussianDiffusion(timesteps=1000)
        
        self.vae_posterior_conv_in = nn.Conv2d(512, 256, 3, padding=1)
        self.vae_posterior_conv_out = nn.Conv2d(256, 8, 3, padding=1)
        
    def encode_text(self, input_ids: torch.Tensor) -> torch.Tensor:
        return self.text_encoder(input_ids)
    
    def forward(self, x_noisy: torch.Tensor, t: torch.Tensor, context: torch.Tensor) -> torch.Tensor:
        return self.unet(x_noisy, t, context)
    
    @torch.no_grad()
    def generate(self, input_ids: torch.Tensor, height: int = 512, width: int = 512, num_inference_steps: int = 50) -> torch.Tensor:
        context = self.encode_text(input_ids)
        
        batch_size = input_ids.shape[0]
        latent_height = height // 8
        latent_width = width // 8
        
        shape = (batch_size, 4, latent_height, latent_width)
        latents = torch.randn(shape, device=input_ids.device)
        
        for t in reversed(range(0, 1000, 1000 // num_inference_steps)):
            t_tensor = torch.full((batch_size,), t, device=input_ids.device, dtype=torch.long)
            predicted_noise = self.unet(latents, t_tensor, context)
            latents = self.diffusion.scheduler.step(predicted_noise, t, latents)
        
        return latents
