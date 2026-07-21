# ============================================
# RockHe — GiMi 0.1 Logger
# ============================================

import sys
import logging
from typing import Any

import structlog

from src.config import config


def setup_logging() -> None:
    """Configure structured logging for RockHe."""
    
    # Standard library logging
    logging.basicConfig(
        format="%(message)s",
        stream=sys.stdout,
        level=getattr(logging, config.LOG_LEVEL.upper(), logging.INFO),
    )
    
    # Structlog processors
    structlog.configure(
        processors=[
            structlog.stdlib.filter_by_level,
            structlog.stdlib.add_logger_name,
            structlog.stdlib.add_log_level,
            structlog.stdlib.PositionalArgumentsFormatter(),
            structlog.processors.TimeStamper(fmt="iso"),
            structlog.processors.StackInfoRenderer(),
            structlog.processors.format_exc_info,
            structlog.processors.UnicodeDecoder(),
            structlog.processors.JSONRenderer() if not config.API_DEBUG else structlog.dev.ConsoleRenderer(),
        ],
        context_class=dict,
        logger_factory=structlog.stdlib.LoggerFactory(),
        wrapper_class=structlog.stdlib.BoundLogger,
        cache_logger_on_first_use=True,
    )


def get_logger(name: str) -> Any:
    """Get a structured logger instance."""
    return structlog.get_logger(name)


# Pre-defined loggers
api_logger = get_logger("rockhe.api")
model_logger = get_logger("rockhe.model")
engine_logger = get_logger("rockhe.gimi")
