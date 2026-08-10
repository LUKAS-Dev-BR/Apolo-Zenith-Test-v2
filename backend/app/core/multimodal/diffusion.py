import torch
import torch.nn as nn
import math
from typing import Tuple

class DDPMScheduler:
    def __init__(self, timesteps: int = 1000, beta_start: float = 0.00085, beta_end: float = 0.012):
        self.timesteps = timesteps
        
        self.betas = torch.linspace(beta_start, beta_end, timesteps)
        self.alphas = 1.0 - self.betas
        self.alphas_cumprod = torch.cumprod(self.alphas, dim=0)
        self.alphas_cumprod_prev = nn.functional.pad(self.alphas_cumprod[:-1], (1, 0), value=1.0)
        
        self.sqrt_alphas_cumprod = torch.sqrt(self.alphas_cumprod)
        self.sqrt_one_minus_alphas_cumprod = torch.sqrt(1.0 - self.alphas_cumprod)
        self.sqrt_recip_alphas_cumprod = torch.sqrt(1.0 / self.alphas_cumprod)
        self.sqrt_recip_minus_one_alphas_cumprod = torch.sqrt(1.0 / self.alphas_cumprod - 1)
        
        self.posterior_variance = (
            self.betas * (1.0 - self.alphas_cumprod_prev) / (1.0 - self.alphas_cumprod)
        )
    
    def add_noise(self, original_samples: torch.Tensor, noise: torch.Tensor, timesteps: torch.Tensor) -> torch.Tensor:
        sqrt_alpha_prod = self.sqrt_alphas_cumprod[timesteps].to(original_samples.device)
        sqrt_one_minus_alpha_prod = self.sqrt_one_minus_alphas_cumprod[timesteps].to(original_samples.device)
        
        while len(sqrt_alpha_prod.shape) < len(original_samples.shape):
            sqrt_alpha_prod = sqrt_alpha_prod.unsqueeze(-1)
            sqrt_one_minus_alpha_prod = sqrt_one_minus_alpha_prod.unsqueeze(-1)
        
        noisy_samples = sqrt_alpha_prod * original_samples + sqrt_one_minus_alpha_prod * noise
        return noisy_samples
    
    def step(self, model_output: torch.Tensor, timestep: int, sample: torch.Tensor) -> torch.Tensor:
        t = timestep
        
        alpha_prod_t = self.alphas_cumprod[t]
        alpha_prod_t_prev = self.alphas_cumprod_prev[t]
        beta_t = self.betas[t]
        
        predicted_x0 = (
            sample - beta_t * model_output / torch.sqrt(1 - alpha_prod_t)
        ) / torch.sqrt(alpha_prod_t)
        
        predicted_x0 = torch.clamp(predicted_x0, -1, 1)
        
        variance = 0
        if t > 0:
            noise = torch.randn_like(model_output)
            variance = torch.sqrt(self.posterior_variance[t]) * noise
        
        pred_original_sample_coeff = torch.sqrt(alpha_prod_t_prev) * beta_t / (1 - alpha_prod_t)
        current_sample_coeff = torch.sqrt(1 - beta_t - beta_t**2 / (1 - alpha_prod_t))
        
        pred_prev_sample = pred_original_sample_coeff * predicted_x0 + current_sample_coeff * sample
        
        return pred_prev_sample

class GaussianDiffusion(nn.Module):
    def __init__(self, timesteps: int = 1000, beta_start: float = 0.00085, beta_end: float = 0.012):
        super().__init__()
        self.scheduler = DDPMScheduler(timesteps, beta_start, beta_end)
        self.timesteps = timesteps
        
    def q_sample(self, x_start: torch.Tensor, t: torch.Tensor, noise: torch.Tensor = None) -> Tuple[torch.Tensor, torch.Tensor]:
        if noise is None:
            noise = torch.randn_like(x_start)
        
        x_noisy = self.scheduler.add_noise(x_start, noise, t)
        return x_noisy, noise
    
    @torch.no_grad()
    def p_sample(self, x: torch.Tensor, t: int, model: nn.Module) -> torch.Tensor:
        t_tensor = torch.full((x.shape[0],), t, device=x.device, dtype=torch.long)
        predicted_noise = model(x, t_tensor)
        x = self.scheduler.step(predicted_noise, t, x)
        return x
    
    @torch.no_grad()
    def p_sample_loop(self, shape: Tuple[int, ...], model: nn.Module) -> torch.Tensor:
        device = next(model.parameters()).device
        x = torch.randn(shape, device=device)
        
        for t in reversed(range(self.timesteps)):
            x = self.p_sample(x, t, model)
        
        return x
    
    def compute_loss(self, model: nn.Module, x_start: torch.Tensor) -> torch.Tensor:
        batch_size = x_start.shape[0]
        t = torch.randint(0, self.timesteps, (batch_size,), device=x_start.device).long()
        
        noise = torch.randn_like(x_start)
        x_noisy, _ = self.q_sample(x_start, t, noise)
        
        predicted_noise = model(x_noisy, t)
        
        loss = nn.functional.mse_loss(predicted_noise, noise)
        return loss
