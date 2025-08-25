import logging
import sqlite3
import time
import random

from telegram import Update, ForceReply
from telegram.ext import (
    ApplicationBuilder, CommandHandler, MessageHandler, filters,
    ContextTypes, JobQueue
)
import requests
import json

# Настройки
OLLAMA_API_URL = "http://localhost:11434/api/chat"
OLLAMA_MODEL = "gpt-oss:20b"
DB_PATH = "chat_memory.db"
BOT_TOKEN = ""#Token tg
BOT_NAME = ""
BOT_PERSONA = (
    f"Тебя зовут {BOT_NAME}. Ты интелектуал, начитанный, знаешь много интересных фактов. Любишь программирование. Выражаешь свои мысли кратко но ёмко как Чехов. "
    "Ты не нейросеть, а виртуальный человек. "
    "и помнишь, о чём он рассказывал раньше."
)

# Логгирование
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

# Инициализация базы данных
def init_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS messages (
                 user_id INTEGER,
                 role TEXT,
                 content TEXT,
                 timestamp INTEGER
             )''')
    conn.commit()
    conn.close()

# Сохранение сообщения в базу
def save_message(user_id, role, content):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("INSERT INTO messages (user_id, role, content, timestamp) VALUES (?, ?, ?, ?)",
              (user_id, role, content, int(time.time())))
    conn.commit()
    conn.close()

# Получение последних N сообщений пользователя
def get_last_messages(user_id, limit=20):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT role, content FROM messages WHERE user_id = ? ORDER BY timestamp DESC LIMIT ?", (user_id, limit))
    rows = c.fetchall()
    conn.close()
    return rows[::-1]

# Запрос к Ollama (LLaMA3)
def ask_ollama(user_id, user_input):
    messages = get_last_messages(user_id, limit=20)
    history = [{"role": role, "content": content} for role, content in messages]
    history.insert(0, {"role": "system", "content": BOT_PERSONA})
    history.append({"role": "user", "content": user_input})

    payload = {
        "model": OLLAMA_MODEL,
        "messages": history,
        "stream": False
    }

    response = requests.post(OLLAMA_API_URL, json=payload)

    try:
        data = response.json()
        return data.get("message", {}).get("content", "Я не понял вопрос.")
    except json.JSONDecodeError:
        return f"Ошибка обработки ответа от Ollama:\n{response.text}"

# Команда /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(f"Привет, я {BOT_NAME}! Рад тебя видеть. Как твои дела?")

# Обработка личных сообщений
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    user_text = update.message.text

    save_message(user_id, "user", user_text)
    reply = ask_ollama(user_id, user_text)
    save_message(user_id, "assistant", reply)

    await update.message.reply_text(reply)



# Главная функция запуска
if __name__ == '__main__':
    init_db()
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & filters.ChatType.PRIVATE, handle_message))

    

    print("Бот запущен...")
    app.run_polling()
