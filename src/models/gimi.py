# ============================================
# RockHe — GiMi 0.1 Engine
# ============================================

import os
from typing import Optional

from src.config import config
from src.models.prompts import get_system_prompt


class GiMiEngine:
    """
    RockHe's local LLM engine.
    Supports multiple backends: llama-cpp, transformers, onnx.
    """
    
    def __init__(self):
        self.model = None
        self.backend = config.MODEL_BACKEND
        self._load_model()
    
    def _load_model(self):
        """Load the local model based on backend setting."""
        
        if self.backend == "llama-cpp":
            self._load_llama_cpp()
        elif self.backend == "transformers":
            self._load_transformers()
        elif self.backend == "onnx":
            self._load_onnx()
        else:
            raise ValueError(f"Unknown backend: {self.backend}")
    
    def _load_llama_cpp(self):
        """Load a GGUF model via llama-cpp-python."""
        from llama_cpp import Llama
        
        model_path = config.MODEL_PATH
        if not model_path or not os.path.exists(model_path):
            raise FileNotFoundError(f"Model not found: {model_path}")
        
        self.model = Llama(
            model_path=model_path,
            n_ctx=config.CONTEXT_WINDOW,
            n_gpu_layers=config.GPU_LAYERS,
            verbose=False,
        )
    
    def _load_transformers(self):
        """Load a HuggingFace model."""
        # TODO: Implement transformers backend
        raise NotImplementedError("Transformers backend coming in GiMi 0.2")
    
    def _load_onnx(self):
        """Load an ONNX model."""
        # TODO: Implement ONNX backend
        raise NotImplementedError("ONNX backend coming in GiMi 0.2")
    
    def generate(
        self,
        message: str,
        history: list[dict],
        temperature: float,
        max_tokens: int,
        persona: str,
    ) -> str:
        """
        Generate a response from the local model.
        
        Args:
            message: User's current message
            history: List of {role, content} dicts
            temperature: Sampling temperature
            max_tokens: Max tokens to generate
            persona: 'general' or 'coding'
        
        Returns:
            Markdown-formatted response string
        """
        
        system_prompt = get_system_prompt(persona)
        
        # Build chat format
        messages = [{"role": "system", "content": system_prompt}]
        messages.extend(history)
        messages.append({"role": "user", "content": message})
        
        # Generate
        if self.backend == "llama-cpp":
            response = self.model.create_chat_completion(
                messages=messages,
                temperature=temperature,
                max_tokens=max_tokens,
            )
            return response["choices"][0]["message"]["content"]
        
        return "GiMi 0.1 is thinking..."  # Fallback


# Singleton instance
_engine: Optional[GiMiEngine] = None


def get_engine() -> GiMiEngine:
    """Get or create the GiMi engine singleton."""
    global _engine
    if _engine is None:
        _engine = GiMiEngine()
    return _engine


async def generate(
    message: str,
    history: list[dict],
    temperature: float,
    max_tokens: int,
    persona: str,
) -> str:
    """
    Async wrapper for generation.
    Called by API routes.
    """
    import asyncio
    
    engine = get_engine()
    
    # Run sync generation in thread pool
    loop = asyncio.get_event_loop()
    return await loop.run_in_executor(
        None,
        engine.generate,
        message,
        history,
        temperature,
        max_tokens,
        persona,
    )
