#!/usr/bin/env python3
"""
Configuration loader – pulls values from environment variables
or `.env` files (if python‑dotenv is installed).
"""

import os
from dataclasses import dataclass
from pathlib import Path

try:
    from dotenv import load_dotenv
    load_dotenv()  # reads .env in project root
except ImportError:  # pragma: no cover
    pass  # dotenv not installed – environment must provide values


@dataclass(frozen=True)
class Config:
    bot_token: str = os.getenv("BOT_TOKEN", "")
    name: str = os.getenv("BOT_NAME", "Бенджамин")
    persona: str = os.getenv("BOT_PERSONA", "")
    ollama_url: str = os.getenv("OLLAMA_URL", "http://localhost:11434/api/chat")
    model: str = os.getenv("OLLAMA_MODEL", "gpt-oss:20b")

    def __post_init__(self):
        missing = [k for k, v in vars(self).items() if not v]
        if missing:
            raise ValueError(f"Missing required config vars: {missing!r}")
