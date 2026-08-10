import torch
import torch.nn as nn
import torch.nn.functional as F
from typing import Tuple, Optional
from app.core.multimodal.diffusion import GaussianDiffusion
from app.core.multimodal.audio import STFTProcessor

class ResBlock1D(nn.Module):
    def __init__(self, in_channels: int, out_channels: int, time_emb_dim: int, kernel_size: int = 3):
        super().__init__()
        self.norm1 = nn.GroupNorm(32, in_channels)
        self.conv1 = nn.Conv1d(in_channels, out_channels, kernel_size, padding=kernel_size // 2)
        self.norm2 = nn.GroupNorm(32, out_channels)
        self.conv2 = nn.Conv1d(out_channels, out_channels, kernel_size, padding=kernel_size // 2)
        
        self.time_mlp = nn.Sequential(
            nn.SiLU(),
            nn.Linear(time_emb_dim, out_channels)
        )
        
        self.residual_conv = nn.Conv1d(in_channels, out_channels, 1) if in_channels != out_channels else nn.Identity()
        
    def forward(self, x: torch.Tensor, time_emb: torch.Tensor) -> torch.Tensor:
        h = self.norm1(x)
        h = F.silu(h)
        h = self.conv1(h)
        
        time_emb = self.time_mlp(time_emb).unsqueeze(-1)
        h = h + time_emb
        
        h = self.norm2(h)
        h = F.silu(h)
        h = self.conv2(h)
        
        return h + self.residual_conv(x)

class DilatedResBlock(nn.Module):
    def __init__(self, channels: int, dilation: int):
        super().__init__()
        self.conv1 = nn.Conv1d(channels, channels, 3, padding=dilation, dilation=dilation)
        self.conv2 = nn.Conv1d(channels, channels, 3, padding=1)
        self.norm1 = nn.GroupNorm(32, channels)
        self.norm2 = nn.GroupNorm(32, channels)
        
    def forward(self, x: torch.Tensor) -> torch.Tensor:
        h = self.norm1(x)
        h = F.silu(h)
        h = self.conv1(h)
        h = self.norm2(h)
        h = F.silu(h)
        h = self.conv2(h)
        return x + h

class HiFiVocoder(nn.Module):
    def __init__(self, in_channels: int = 1, base_channels: int = 512, upsample_rates: Tuple = (8, 8, 2, 2), upsample_kernel_sizes: Tuple = (16, 16, 4, 4)):
        super().__init__()
        
        self.conv_in = nn.Conv1d(in_channels, base_channels, 7, padding=3)
        
        self.upsample_blocks = nn.ModuleList()
        curr_channels = base_channels
        
        for i, (rate, kernel) in enumerate(zip(upsample_rates, upsample_kernel_sizes)):
            out_channels = base_channels // (2 ** (i + 1))
            self.upsample_blocks.append(nn.ModuleList([
                nn.ConvTranspose1d(curr_channels, out_channels, kernel, stride=rate, padding=(kernel - rate) // 2),
                ResBlock1D(out_channels, out_channels, 512),
                ResBlock1D(out_channels, out_channels, 512)
            ]))
            curr_channels = out_channels
        
        self.dilated_blocks = nn.ModuleList([
            DilatedResBlock(curr_channels, 1),
            DilatedResBlock(curr_channels, 3),
            DilatedResBlock(curr_channels, 9),
            DilatedResBlock(curr_channels, 27)
        ])
        
        self.conv_out = nn.Conv1d(curr_channels, 1, 7, padding=3)
        self.tanh = nn.Tanh()
        
    def forward(self, x: torch.Tensor) -> torch.Tensor:
        h = self.conv_in(x)
        
        for upsample, res1, res2 in self.upsample_blocks:
            h = upsample(h)
            h = res1(h, torch.randn(h.shape[0], 512, device=h.device))
            h = res2(h, torch.randn(h.shape[0], 512, device=h.device))
        
        for block in self.dilated_blocks:
            h = block(h)
        
        h = self.conv_out(h)
        h = self.tanh(h)
        
        return h

class UNet2DMusic(nn.Module):
    def __init__(self, in_channels: int = 1, base_channels: int = 128, channel_mults: Tuple = (1, 2, 4, 8), time_emb_dim: int = 512, context_dim: int = 768):
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
                ResBlock2D(curr_channels, out_channels, time_emb_dim),
                CrossAttention2D(out_channels, context_dim),
                ResBlock2D(out_channels, out_channels, time_emb_dim)
            ]))
            channels.append(out_channels)
            curr_channels = out_channels
            self.down_samples.append(nn.Conv2d(out_channels, out_channels, 3, stride=2, padding=1))
        
        self.mid_block1 = ResBlock2D(curr_channels, curr_channels, time_emb_dim)
        self.mid_attn = CrossAttention2D(curr_channels, context_dim)
        self.mid_block2 = ResBlock2D(curr_channels, curr_channels, time_emb_dim)
        
        self.up_blocks = nn.ModuleList()
        self.up_samples = nn.ModuleList()
        
        for mult in reversed(channel_mults):
            out_channels = base_channels * mult
            self.up_blocks.append(nn.ModuleList([
                ResBlock2D(curr_channels + channels.pop(), out_channels, time_emb_dim),
                CrossAttention2D(out_channels, context_dim),
                ResBlock2D(out_channels, out_channels, time_emb_dim)
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

class TextEncoder(nn.Module):
    def __init__(self, vocab_size: int = 32000, d_model: int = 768, n_heads: int = 12, n_layers: int = 6, max_seq_len: int = 256):
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

class TextToMusicPipeline(nn.Module):
    def __init__(self, vocab_size: int = 32000, d_model: int = 768, sample_rate: int = 22050, n_mels: int = 80):
        super().__init__()
        
        self.sample_rate = sample_rate
        self.n_mels = n_mels
        
        self.text_encoder = TextEncoder(vocab_size, d_model)
        self.unet = UNet2DMusic(in_channels=1, base_channels=128, context_dim=d_model)
        self.vocoder = HiFiVocoder(in_channels=1, base_channels=512)
        self.diffusion = GaussianDiffusion(timesteps=1000)
        self.stft_processor = STFTProcessor(sample_rate, n_mels=n_mels)
        
    def encode_text(self, input_ids: torch.Tensor) -> torch.Tensor:
        return self.text_encoder(input_ids)
    
    def forward(self, x_noisy: torch.Tensor, t: torch.Tensor, context: torch.Tensor) -> torch.Tensor:
        return self.unet(x_noisy, t, context)
    
    @torch.no_grad()
    def generate(self, input_ids: torch.Tensor, duration_seconds: float = 30.0, bpm: int = 120, num_inference_steps: int = 50) -> torch.Tensor:
        context = self.encode_text(input_ids)
        
        batch_size = input_ids.shape[0]
        num_samples = int(duration_seconds * self.sample_rate)
        num_frames = num_samples // 256 + 1
        
        shape = (batch_size, 1, self.n_mels, num_frames)
        latents = torch.randn(shape, device=input_ids.device)
        
        for t in reversed(range(0, 1000, 1000 // num_inference_steps)):
            t_tensor = torch.full((batch_size,), t, device=input_ids.device, dtype=torch.long)
            predicted_noise = self.unet(latents, t_tensor, context)
            latents = self.diffusion.scheduler.step(predicted_noise, t, latents)
        
        wav = self.stft_processor.spectrogram_to_wav(latents.squeeze(1), num_samples)
        wav = self.vocoder(wav.unsqueeze(1))
        
        return wav.squeeze(1)
    
    def save_wav(self, wav: torch.Tensor, path: str):
        import torchaudio
        torchaudio.save(path, wav.cpu(), self.sample_rate)
