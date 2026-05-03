import os
from flask import Flask
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, ContextTypes, filters

# ===== 基本設定 =====
TOKEN = os.getenv("BOT_TOKEN")

GROUP_ID = -5105827693
ALLOWED_USERS = [1165688271]

# ===== Flask（讓 Render 不會報 no port）=====
app = Flask(__name__)

@app.route("/")
def home():
    return "Bot is running"

def run_web():
    app.run(host="0.0.0.0", port=10000)

# ===== Telegram Bot 邏輯 =====
async def relay(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message:
        return

    user_id = update.message.from_user.id
    text = update.message.text

    print("收到訊息:", text)

    # 白名單
    if user_id not in ALLOWED_USERS:
        print("非白名單使用者:", user_id)
        return

    # 轉傳到群組
    await context.bot.send_message(chat_id=GROUP_ID, text=text)

# ===== 啟動 bot =====
def run_bot():
    application = ApplicationBuilder().token(TOKEN).build()

    application.add_handler(
        MessageHandler(filters.TEXT & ~filters.COMMAND, relay)
    )

    print("Bot 已啟動")

    application.run_polling()

# ===== 同時啟動 web + bot =====
if __name__ == "__main__":
    import threading

    threading.Thread(target=run_web).start()
    run_bot()
