#!/usr/bin/env python3
"""
Telegram Bot that talks to an Ollama LLM and remembers conversation history.

"""

import logging
import random
import time
from pathlib import Path
from typing import List, Tuple

import requests
from telegram import Update
from telegram.constants import ChatType
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    Filters,
    MessageHandler,
    ContextTypes,
)

from config import Config
from db import ConversationDB

# --------------------------------------------------------------------------- #
# Logging
# --------------------------------------------------------------------------- #
logging.basicConfig(
    format="%(asctime)s — %(levelname)s — %(name)s — %(message)s",
    level=logging.INFO,
)
logger = logging.getLogger(__name__)

# --------------------------------------------------------------------------- #
# Global objects
# --------------------------------------------------------------------------- #
config = Config()
db = ConversationDB()

# --------------------------------------------------------------------------- #
# Utility functions
# --------------------------------------------------------------------------- #
def _assemble_history(user_id: int, limit: int = 10) -> List[dict]:
    """Retrieve the last *limit* exchanges and turn them into the format
    expected by Ollama.
    """
    rows = db.get_last_messages(user_id, limit=limit)
    history = [{"role": r[0], "content": r[1]} for r in rows]
    history.insert(0, {"role": "system", "content": config.persona})
    return history


def _ask_ollama(user_id: int, user_input: str) -> str:
    """Send a request to the Ollama server and return the answer."""
    history = _assemble_history(user_id)
    history.append({"role": "user", "content": user_input})

    payload = {
        "model": config.model,
        "messages": history,
        "stream": False,
    }

    try:
        r = requests.post(config.ollama_url, json=payload, timeout=30)
        r.raise_for_status()
    except requests.RequestException as exc:
        logger.exception("Failure during Ollama request")
        return f"❌ Unable to reach the model server: {exc}"

    try:
        data = r.json()
        return data.get("message", {}).get("content", "Я не понял твой вопрос.")
    except ValueError as exc:
        logger.exception("Invalid JSON response from Ollama")
        return f"❌ Ошибка обработки ответа: {exc}"


# --------------------------------------------------------------------------- #
# Handlers
# --------------------------------------------------------------------------- #
async def start(update: Update, *_: ContextTypes.DEFAULT_TYPE) -> None:
    """Respond to /start."""
    await update.message.reply_text(
        f"Привет, я {config.name}! Как настроение?"
    )




# --------------------------------------------------------------------------- #
# Application bootstrap
# --------------------------------------------------------------------------- #
def main() -> None:
    db.init()
    app = ApplicationBuilder().token(config.bot_token).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(Filters.TEXT & Filters.ChatType.private, _handle_message))
 

    logger.info("Bot is up and running")
    app.run_polling()


if __name__ == "__main__":
    main()
