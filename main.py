import os
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes
from flask import Flask
import threading

TOKEN = os.getenv("BOT_TOKEN")
GROUP_ID = -5105827693
ALLOWED_USERS = [1165688271]

# ===== Telegram Bot =====
async def relay(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    text = update.message.text

    if user_id not in ALLOWED_USERS:
        return

    await context.bot.send_message(chat_id=GROUP_ID, text=text)

def run_bot():
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, relay))
    app.run_polling()

# ===== Fake Web Server (給 Render 用) =====
web = Flask("")

@web.route("/")
def home():
    return "Bot is running"

def run_web():
    web.run(host="0.0.0.0", port=10000)

# ===== 同時啟動 =====
threading.Thread(target=run_bot).start()
threading.Thread(target=run_web).start()
