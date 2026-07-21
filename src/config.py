# ============================================
# RockHe — GiMi 0.1 Configuration
# ============================================

import os
from pathlib import Path
from dotenv import load_dotenv

# Load .env from project root
BASE_DIR = Path(__file__).resolve().parent.parent.parent
load_dotenv(BASE_DIR / ".env")


class Config:
    """RockHe configuration. All values pulled from .env (blank = unset)."""

    # --- Model ---
    MODEL_PATH: str = os.getenv("MODEL_PATH", "")
    MODEL_BACKEND: str = os.getenv("MODEL_BACKEND", "llama-cpp")
    MODEL_FILENAME: str = os.getenv("MODEL_FILENAME", "")

    # --- API Server ---
    API_HOST: str = os.getenv("API_HOST", "0.0.0.0")
    API_PORT: int = int(os.getenv("API_PORT", "8000"))
    API_DEBUG: bool = os.getenv("API_DEBUG", "false").lower() == "true"

    CORS_ORIGINS: list[str] = [
        origin.strip()
        for origin in os.getenv("CORS_ORIGINS", "http://localhost:3000").split(",")
        if origin.strip()
    ]

    # --- GiMi Engine ---
    MAX_TOKENS: int = int(os.getenv("MAX_TOKENS", "2048"))
    TEMPERATURE: float = float(os.getenv("TEMPERATURE", "0.7"))
    PERSONA: str = os.getenv("PERSONA", "general")
    CONTEXT_WINDOW: int = int(os.getenv("CONTEXT_WINDOW", "4096"))

    # --- Hardware ---
    GPU_LAYERS: int = int(os.getenv("GPU_LAYENS", "-1"))
    DEVICE: str = os.getenv("DEVICE", "cpu")

    # --- Logging ---
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")

    # --- Rate Limiting ---
    RATE_LIMIT_RPM: int = int(os.getenv("RATE_LIMIT_RPM", "60"))


# Singleton instance
config = Config()
