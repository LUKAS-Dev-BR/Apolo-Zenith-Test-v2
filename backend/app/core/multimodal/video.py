import torch
import torch.nn as nn
import torch.nn.functional as F
from typing import Tuple, Optional
from app.core.multimodal.diffusion import GaussianDiffusion

class TemporalAttention(nn.Module):
    def __init__(self, channels: int, num_heads: int = 8):
        super().__init__()
        self.num_heads = num_heads
        self.head_dim = channels // num_heads
        
        self.norm = nn.GroupNorm(32, channels)
        self.q = nn.Linear(channels, channels)
        self.k = nn.Linear(channels, channels)
        self.v = nn.Linear(channels, channels)
        self.out = nn.Linear(channels, channels)
        
    def forward(self, x: torch.Tensor) -> torch.Tensor:
        batch_size, channels, frames, height, width = x.shape
        
        h = self.norm(x)
        h = h.permute(0, 3, 4, 1, 2).contiguous()
        h = h.view(batch_size * height * width, channels, frames)
        h = h.permute(0, 2, 1)
        
        q = self.q(h)
        k = self.k(h)
        v = self.v(h)
        
        q = q.view(batch_size * height * width, frames, self.num_heads, self.head_dim).permute(0, 2, 1, 3)
        k = k.view(batch_size * height * width, frames, self.num_heads, self.head_dim).permute(0, 2, 1, 3)
        v = v.view(batch_size * height * width, frames, self.num_heads, self.head_dim).permute(0, 2, 1, 3)
        
        attn = torch.matmul(q, k.transpose(-2, -1)) / (self.head_dim ** 0.5)
        attn = F.softmax(attn, dim=-1)
        
        out = torch.matmul(attn, v)
        out = out.permute(0, 2, 1, 3).contiguous()
        out = out.view(batch_size * height * width, frames, channels)
        out = out.permute(0, 2, 1)
        out = self.out(out)
        
        out = out.view(batch_size, height, width, channels, frames)
        out = out.permute(0, 4, 3, 1, 2)
        
        return x + out

class ResBlock3D(nn.Module):
    def __init__(self, in_channels: int, out_channels: int, time_emb_dim: int):
        super().__init__()
        self.norm1 = nn.GroupNorm(32, in_channels)
        self.conv1 = nn.Conv3d(in_channels, out_channels, 3, padding=1)
        self.norm2 = nn.GroupNorm(32, out_channels)
        self.conv2 = nn.Conv3d(out_channels, out_channels, 3, padding=1)
        
        self.time_mlp = nn.Sequential(
            nn.SiLU(),
            nn.Linear(time_emb_dim, out_channels)
        )
        
        self.residual_conv = nn.Conv3d(in_channels, out_channels, 1) if in_channels != out_channels else nn.Identity()
        
    def forward(self, x: torch.Tensor, time_emb: torch.Tensor) -> torch.Tensor:
        h = self.norm1(x)
        h = F.silu(h)
        h = self.conv1(h)
        
        time_emb = self.time_mlp(time_emb)
        time_emb = time_emb.unsqueeze(-1).unsqueeze(-1).unsqueeze(-1)
        h = h + time_emb
        
        h = self.norm2(h)
        h = F.silu(h)
        h = self.conv2(h)
        
        return h + self.residual_conv(x)

class CrossAttention3D(nn.Module):
    def __init__(self, channels: int, context_dim: int, num_heads: int = 8):
        super().__init__()
        self.num_heads = num_heads
        self.head_dim = channels // num_heads
        
        self.norm = nn.GroupNorm(32, channels)
        self.q = nn.Conv3d(channels, channels, 1)
        self.k = nn.Linear(context_dim, channels)
        self.v = nn.Linear(context_dim, channels)
        self.out = nn.Conv3d(channels, channels, 1)
        
    def forward(self, x: torch.Tensor, context: torch.Tensor) -> torch.Tensor:
        batch_size, channels, frames, height, width = x.shape
        
        h = self.norm(x)
        q = self.q(h).view(batch_size, self.num_heads, self.head_dim, frames, height * width)
        q = q.permute(0, 1, 3, 4, 2)
        
        k = self.k(context).view(batch_size, -1, self.num_heads, self.head_dim).permute(0, 2, 1, 3)
        v = self.v(context).view(batch_size, -1, self.num_heads, self.head_dim).permute(0, 2, 1, 3)
        
        q = q.reshape(batch_size * self.num_heads * frames, height * width, self.head_dim)
        k = k.unsqueeze(2).expand(-1, -1, frames, -1).reshape(batch_size * self.num_heads * frames, -1, self.head_dim)
        v = v.unsqueeze(2).expand(-1, -1, frames, -1).reshape(batch_size * self.num_heads * frames, -1, self.head_dim)
        
        attn = torch.bmm(q, k.transpose(-2, -1)) / (self.head_dim ** 0.5)
        attn = F.softmax(attn, dim=-1)
        
        out = torch.bmm(attn, v)
        out = out.view(batch_size, self.num_heads, frames, height * width, self.head_dim)
        out = out.permute(0, 1, 4, 3, 2)
        out = out.reshape(batch_size, channels, frames, height, width)
        out = self.out(out)
        
        return x + out

class UNet3D(nn.Module):
    def __init__(self, in_channels: int = 4, base_channels: int = 128, channel_mults: Tuple = (1, 2, 4), time_emb_dim: int = 512, context_dim: int = 768):
        super().__init__()
        
        self.time_mlp = nn.Sequential(
            nn.Linear(128, time_emb_dim),
            nn.SiLU(),
            nn.Linear(time_emb_dim, time_emb_dim)
        )
        
        self.input_conv = nn.Conv3d(in_channels, base_channels, 3, padding=1)
        
        self.down_blocks = nn.ModuleList()
        self.down_temporal = nn.ModuleList()
        self.down_samples = nn.ModuleList()
        
        channels = [base_channels]
        curr_channels = base_channels
        
        for mult in channel_mults:
            out_channels = base_channels * mult
            self.down_blocks.append(nn.ModuleList([
                ResBlock3D(curr_channels, out_channels, time_emb_dim),
                CrossAttention3D(out_channels, context_dim),
                ResBlock3D(out_channels, out_channels, time_emb_dim)
            ]))
            self.down_temporal.append(TemporalAttention(out_channels))
            channels.append(out_channels)
            curr_channels = out_channels
            self.down_samples.append(nn.Conv3d(out_channels, out_channels, 3, stride=(1, 2, 2), padding=1))
        
        self.mid_block1 = ResBlock3D(curr_channels, curr_channels, time_emb_dim)
        self.mid_attn = CrossAttention3D(curr_channels, context_dim)
        self.mid_temporal = TemporalAttention(curr_channels)
        self.mid_block2 = ResBlock3D(curr_channels, curr_channels, time_emb_dim)
        
        self.up_blocks = nn.ModuleList()
        self.up_temporal = nn.ModuleList()
        self.up_samples = nn.ModuleList()
        
        for mult in reversed(channel_mults):
            out_channels = base_channels * mult
            self.up_blocks.append(nn.ModuleList([
                ResBlock3D(curr_channels + channels.pop(), out_channels, time_emb_dim),
                CrossAttention3D(out_channels, context_dim),
                ResBlock3D(out_channels, out_channels, time_emb_dim)
            ]))
            self.up_temporal.append(TemporalAttention(out_channels))
            self.up_samples.append(nn.ConvTranspose3d(out_channels, out_channels, (1, 4, 4), stride=(1, 2, 2), padding=(0, 1, 1)))
            curr_channels = out_channels
        
        self.output_norm = nn.GroupNorm(32, curr_channels)
        self.output_conv = nn.Conv3d(curr_channels, in_channels, 3, padding=1)
        
    def forward(self, x: torch.Tensor, t: torch.Tensor, context: Optional[torch.Tensor] = None) -> torch.Tensor:
        batch_size = x.shape[0]
        
        t_emb = torch.randn(batch_size, 128, device=x.device)
        t_emb = self.time_mlp(t_emb)
        
        h = self.input_conv(x)
        
        residuals = [h]
        
        for i, (block, attn, block2) in enumerate(self.down_blocks):
            h = block(h, t_emb)
            if context is not None:
                h = attn(h, context)
            h = block2(h, t_emb)
            h = self.down_temporal[i](h)
            residuals.append(h)
            h = self.down_samples[i](h)
        
        h = self.mid_block1(h, t_emb)
        if context is not None:
            h = self.mid_attn(h, context)
        h = self.mid_temporal(h)
        h = self.mid_block2(h, t_emb)
        
        for i, (block, attn, block2) in enumerate(self.up_blocks):
            h = self.up_samples[i](h)
            h = torch.cat([h, residuals.pop()], dim=1)
            h = block(h, t_emb)
            if context is not None:
                h = attn(h, context)
            h = block2(h, t_emb)
            h = self.up_temporal[i](h)
        
        h = self.output_norm(h)
        h = F.silu(h)
        h = self.output_conv(h)
        
        return h

class TextToVideoPipeline(nn.Module):
    def __init__(self, vocab_size: int = 32000, d_model: int = 768):
        super().__init__()
        
        from app.core.multimodal.image import CLIPTextEncoder
        self.text_encoder = CLIPTextEncoder(vocab_size, d_model)
        self.unet = UNet3D(in_channels=4, base_channels=128, context_dim=d_model)
        self.diffusion = GaussianDiffusion(timesteps=1000)
        
    def encode_text(self, input_ids: torch.Tensor) -> torch.Tensor:
        return self.text_encoder(input_ids)
    
    def forward(self, x_noisy: torch.Tensor, t: torch.Tensor, context: torch.Tensor) -> torch.Tensor:
        return self.unet(x_noisy, t, context)
    
    @torch.no_grad()
    def generate(self, input_ids: torch.Tensor, height: int = 256, width: int = 256, num_frames: int = 16, num_inference_steps: int = 50) -> torch.Tensor:
        context = self.encode_text(input_ids)
        
        batch_size = input_ids.shape[0]
        latent_height = height // 8
        latent_width = width // 8
        
        shape = (batch_size, 4, num_frames, latent_height, latent_width)
        latents = torch.randn(shape, device=input_ids.device)
        
        for t in reversed(range(0, 1000, 1000 // num_inference_steps)):
            t_tensor = torch.full((batch_size,), t, device=input_ids.device, dtype=torch.long)
            predicted_noise = self.unet(latents, t_tensor, context)
            latents = self.diffusion.scheduler.step(predicted_noise, t, latents)
        
        return latents
