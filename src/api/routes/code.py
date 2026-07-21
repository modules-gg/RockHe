# ============================================
# RockHe — GiMi 0.1 Code Route
# ============================================

from fastapi import APIRouter, Request, HTTPException

from src.config import config
from src.api.schemas import CodeRequest, ChatResponse
from src.models.gimi import generate

router = APIRouter()


@router.post("/", response_model=ChatResponse)
async def code(request: Request, body: CodeRequest):
    """
    Coding assistant endpoint.
    Optimized for code generation, debugging, and explanation.
    Returns Markdown with syntax-highlighted code blocks.
    """
    
    # Build coding-specific prompt
    language_hint = f" in {body.language}" if body.language else ""
    enhanced_message = (
        f"Write clean, well-commented code{language_hint} for the following task. "
        f"Use Markdown code blocks with the correct language tag. "
        f"Explain briefly after the code.\n\nTask: {body.message}"
    )
    
    try:
        response_text = await generate(
            message=enhanced_message,
            history=body.history or [],
            temperature=body.temperature or config.TEMPERATURE,
            max_tokens=body.max_tokens or config.MAX_TOKENS,
            persona="coding",
        )
        
        return ChatResponse(
            response=response_text,
            tokens_used=0,  # TODO: count tokens
            model="gimi-0.1",
            finish_reason="stop",
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
