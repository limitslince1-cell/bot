import os
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


# ===== Bot =====
async def relay(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message:
        return

    user_id = update.message.from_user.id

    print("收到:", update.message, flush=True)

    # 白名單
    if user_id not in ALLOWED_USERS:
        return

    # 👉 直接 forward（重點！！）
    await update.message.forward(chat_id=GROUP_ID)


def run_web():
    app_web.run(host="0.0.0.0", port=10000)


def run_bot():
    app = ApplicationBuilder().token(TOKEN).build()

    # 👉 全部訊息都接
    app.add_handler(MessageHandler(filters.ALL, relay))

    print("Bot started", flush=True)
    app.run_polling()


if __name__ == "__main__":
    run_bot()
