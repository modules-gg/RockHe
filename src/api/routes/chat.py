# ============================================
# RockHe — GiMi 0.1 Chat Route
# ============================================

from fastapi import APIRouter, Request, HTTPException
from slowapi.util import get_remote_address

from src.config import config
from src.api.schemas import ChatRequest, ChatResponse
from src.models.gimi import generate

router = APIRouter()


@router.post("/", response_model=ChatResponse)
async def chat(request: Request, body: ChatRequest):
    """
    General conversation endpoint.
    Returns Markdown-formatted text.
    """
    
    # TODO: Wire to actual model once gimi.py is implemented
    # For now, return a placeholder
    
    try:
        response_text = await generate(
            message=body.message,
            history=body.history or [],
            temperature=body.temperature or config.TEMPERATURE,
            max_tokens=body.max_tokens or config.MAX_TOKENS,
            persona="general",
        )
        
        return ChatResponse(
            response=response_text,
            tokens_used=0,  # TODO: count tokens
            model="gimi-0.1",
            finish_reason="stop",
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
