# 🤖 Telegram Bot with Ollama (LLM Integration)

This project is a **Telegram chatbot** powered by a local **LLM (Large Language Model)** through [Ollama](https://ollama.ai/).  
The bot acts like a virtual human: it remembers conversation history, has a custom persona, and interacts naturally with users.

---

## ✨ Features
- Stores conversation history in **SQLite**.
- Maintains context between messages.
- Responds with a custom **persona**.
- Runs locally using **Ollama** models.
- Simple and lightweight setup.

---

## 📦 Installation

### 1. Install dependencies
```bash
pip install python-telegram-bot==20.7 requests
SQLite comes preinstalled with Python.
```
2. Install and run Ollama
Download Ollama: https://ollama.ai/download

Start the server:

ollama serve
Pull a model of your choice (for example gpt-oss:20b or llama3:8b):

```bash

ollama pull gpt-oss:20b
```
3. Create a Telegram Bot
Open @BotFather in Telegram.

Use /newbot to create a bot and get your API token.

Paste the token into the BOT_TOKEN variable in the code.

⚙️ Configuration
At the top of main.py, update the settings:

```python

OLLAMA_API_URL = "http://localhost:11434/api/chat"  # Ollama server URL
OLLAMA_MODEL = "gpt-oss:20b"  # Model to use
DB_PATH = "chat_memory.db"     # SQLite database file
BOT_TOKEN = "YOUR_TELEGRAM_BOT_TOKEN"
BOT_NAME = "Benjamin"          # Bot persona name

```
You can also customize the persona in BOT_PERSONA to adjust how the bot behaves.

🚀 Run the bot
Run:

```bash

python main.py
```
If everything is set up correctly, you will see:
Bot started...

📂 Project structure
bash

main.py          # Bot source code
chat_memory.db   # SQLite database with chat history
README.md        # Documentation

💡 Tips
For faster responses, use quantized models (e.g. llama3:8b-q4_K_M).

Start testing in private chat with your bot before wider use.

Conversation history is stored locally in chat_memory.db — you can reset it by deleting the file.
