# Telegram + Ollama Chat Bot

A lightweight Telegram bot that delegates every query to an Ollama LLM,
keeps conversation history locally, and can be extended easily.

## Features

- **Stateful conversations** – last 10 exchanges are sent with every request.
- **Custom persona** – set the system prompt via `BOT_PERSONA`.
- **Optional periodic chatter** – send a ping every N seconds in a group.
- **Docker‑friendly** – just expose the environment variables.

## Getting Started

```bash
# Git clone
git clone https://github.com/youruser/telegram-ollama-bot.git
cd telegram-ollama-bot

# (Optional) Set up a virtual environment
python3 -m venv .venv
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Create a `.env` file:
cat <<EOF > .env
BOT_TOKEN="123456:ABC-DEF1234ghIkl-zyx57W2v1u123ew11"
BOT_NAME="Бенджамин"
BOT_PERSONA="Ты всегда отвечаешь с точки зрения дружелюбного инженера."
OLLAMA_URL="http://localhost:11434/api/chat"
OLLAMA_MODEL="gpt-oss:20b"
EOF

# Run the bot
python telegram_bot.py
