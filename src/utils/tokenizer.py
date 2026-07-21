# ============================================
# RockHe — GiMi 0.1 Tokenizer Utility
# ============================================

import re
from typing import List


def count_tokens(text: str) -> int:
    """
    Rough token count for local models.
    ~0.75 words per token (approximation for English).
    """
    if not text:
        return 0
    
    # Split on whitespace and punctuation
    words = re.findall(r"\w+|[^\w\s]", text)
    return int(len(words) / 0.75)


def truncate_to_tokens(text: str, max_tokens: int) -> str:
    """
    Truncate text to fit within max_tokens.
    """
    if count_tokens(text) <= max_tokens:
        return text
    
    words = text.split()
    target_words = int(max_tokens * 0.75)
    return " ".join(words[:target_words]) + "..."


def encode_chat(messages: List[dict]) -> str:
    """
    Convert chat history to a single string for model input.
    """
    formatted = []
    for msg in messages:
        role = msg.get("role", "user")
        content = msg.get("content", "")
        formatted.append(f"<|{role}|>\n{content}")
    
    return "\n".join(formatted) + "\n<|assistant|>\n"


def estimate_context_fit(messages: List[dict], max_context: int) -> bool:
    """
    Check if messages fit within the context window.
    """
    text = encode_chat(messages)
    return count_tokens(text) <= max_context
