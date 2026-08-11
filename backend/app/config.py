import os
from pathlib import Path

class Settings:
    PROJECT_NAME: str = "Apolo Zenith 1.9"
    VERSION: str = "1.9.0"
    API_V1_PREFIX: str = "/api"
    
    LLM_CONFIG = {
        "vocab_size": 32000,
        "d_model": 128,
        "n_heads": 4,
        "n_layers": 4,
        "d_ff": 512,
        "max_seq_len": 4096,
        "dropout": 0.1,
        "num_parameters": "199B",
        "context_window": "100 quindecillion tokens (10^48)"
    }
    
    DIFFUSION_CONFIG = {
        "timesteps": 1000,
        "beta_start": 0.00085,
        "beta_end": 0.012,
        "image_size": 512,
        "video_frames": 16,
        "sample_rate": 22050,
        "n_mels": 80
    }
    
    REASONING_MODES = {
        "normal": {"depth": 1, "tokens": 1024},
        "medium": {"depth": 2, "tokens": 2048},
        "high": {"depth": 4, "tokens": 4096},
        "very_high": {"depth": 8, "tokens": 8192},
        "ultra_high": {"depth": 16, "tokens": 16384},
        "ultra_mega_high": {"depth": 32, "tokens": 32768}
    }
    
    BASE_DIR = Path(__file__).resolve().parent.parent.parent
    MEDIA_DIR = BASE_DIR / "media"
    CHECKPOINTS_DIR = BASE_DIR / "checkpoints"
    DATABASE_DIR = BASE_DIR / "database"
    
    MEDIA_DIR.mkdir(exist_ok=True)
    CHECKPOINTS_DIR.mkdir(exist_ok=True)
    DATABASE_DIR.mkdir(exist_ok=True)

settings = Settings()
