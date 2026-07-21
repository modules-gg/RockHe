# ============================================
# RockHe — GiMi 0.1 API Schemas
# ============================================

from pydantic import BaseModel, Field
from typing import Optional


class ChatRequest(BaseModel):
    """Incoming message from the user."""
    
    message: str = Field(
        ...,
        min_length=1,
        max_length=8192,
        description="The user's text input",
    )
    
    history: Optional[list[dict]] = Field(
        default=None,
        description="Optional conversation history: [{role, content}, ...]",
    )
    
    temperature: Optional[float] = Field(
        default=None,
        ge=0.0,
        le=2.0,
        description="Override default temperature",
    )
    
    max_tokens: Optional[int] = Field(
        default=None,
        ge=1,
        le=32768,
        description="Override default max tokens",
    )


class CodeRequest(BaseModel):
    """Incoming coding task from the user."""
    
    message: str = Field(
        ...,
        min_length=1,
        max_length=8192,
        description="The coding task or question",
    )
    
    language: Optional[str] = Field(
        default=None,
        description="Target programming language (e.g., 'python', 'rust')",
    )
    
    history: Optional[list[dict]] = Field(
        default=None,
        description="Optional conversation history",
    )


class ChatResponse(BaseModel):
    """AI response back to the user."""
    
    response: str = Field(
        ...,
        description="The AI's Markdown-formatted response",
    )
    
    tokens_used: int = Field(
        ...,
        ge=0,
        description="Tokens consumed for this response",
    )
    
    model: str = Field(
        default="gimi-0.1",
        description="Model identifier",
    )
    
    finish_reason: Optional[str] = Field(
        default=None,
        description="Why generation stopped: 'stop', 'length', 'error'",
    )


class HealthResponse(BaseModel):
    """Server status check."""
    
    name: str
    version: str
    status: str
    model_loaded: bool
