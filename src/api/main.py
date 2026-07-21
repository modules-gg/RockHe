# ============================================
# RockHe — GiMi 0.1 API Server
# ============================================

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded

from src.config import config
from src.api.routes import chat, code

# --- Rate Limiter ---
limiter = Limiter(key_func=get_remote_address)

# --- App Instance ---
app = FastAPI(
    title="RockHe — GiMi 0.1",
    description="Local AI API for coding and general tasks. Text-only. Markdown-native.",
    version="0.1.0",
)

app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

# --- CORS ---
app.add_middleware(
    CORSMiddleware,
    allow_origins=config.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- Routes ---
app.include_router(chat.router, prefix="/chat", tags=["Chat"])
app.include_router(code.router, prefix="/code", tags=["Code"])


# --- Health Check ---
@app.get("/")
@limiter.limit(f"{config.RATE_LIMIT_RPM}/minute")
async def root(request: Request):
    return {
        "name": "RockHe",
        "version": "0.1.0",
        "status": "alive",
        "model_loaded": False,  # TODO: wire to gimi.py
    }


# --- Startup / Shutdown ---
@app.on_event("startup")
async def startup():
    print(f"🪨 RockHe GiMi 0.1 starting on {config.API_HOST}:{config.API_PORT}")
    print(f"   Model backend: {config.MODEL_BACKEND}")
    print(f"   Device: {config.DEVICE}")
    # TODO: Load model here


@app.on_event("shutdown")
async def shutdown():
    print("🪨 RockHe shutting down.")
    # TODO: Unload model here
