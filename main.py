import os
import threading
from flask import Flask
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, ContextTypes, filters

TOKEN = os.getenv("BOT_TOKEN")

GROUP_ID = -5105827693
ALLOWED_USERS = [1165688271]

app_web = Flask(__name__)

@app_web.route("/")
def home():
    return "OK"

# ===== bot =====
async def relay(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message:
        return

    user_id = update.message.from_user.id
    text = update.message.text

    print("收到:", text, flush=True)

    if user_id not in ALLOWED_USERS:
        return

    await context.bot.send_message(chat_id=GROUP_ID, text=text)

def run_web():
    app_web.run(host="0.0.0.0", port=10000)

def run_bot():
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, relay))

    print("Bot started", flush=True)
    app.run_polling()

if __name__ == "__main__":
    # 👉 Flask 丟去背景
    threading.Thread(target=run_web).start()

    # 👉 Bot 一定要在主線程（超重要）
    run_bot()
