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

# =======================
# Telegram handler
# =======================
async def relay(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message:
        return

    user_id = update.message.from_user.id

    # 🔐 白名單
    if user_id not in ALLOWED_USERS:
        return

    msg = update.message

    # ===== 文字 =====
    if msg.text:
        await context.bot.send_message(chat_id=GROUP_ID, text=msg.text)

    # ===== 圖片 =====
    elif msg.photo:
        photo = msg.photo[-1].file_id
        await context.bot.send_photo(chat_id=GROUP_ID, photo=photo, caption=msg.caption or "")

    # ===== 貼圖 =====
    elif msg.sticker:
        await context.bot.send_sticker(chat_id=GROUP_ID, sticker=msg.sticker.file_id)

    # ===== GIF / 動圖 =====
    elif msg.animation:
        await context.bot.send_animation(chat_id=GROUP_ID, animation=msg.animation.file_id, caption=msg.caption or "")

    print("收到訊息:", user_id, flush=True)


def run_web():
    # Render 必須 bind 0.0.0.0
    port = int(os.environ.get("PORT", 10000))
    app_web.run(host="0.0.0.0", port=port)


def run_bot():
    app = ApplicationBuilder().token(TOKEN).build()

    # 支援所有訊息類型
    app.add_handler(MessageHandler(filters.ALL, relay))

    print("Bot started", flush=True)

    # ⭐ 重點：避免舊訊息 + 提高穩定性
    app.run_polling(drop_pending_updates=True)


if __name__ == "__main__":
    from threading import Thread

    # Flask 放背景
    Thread(target=run_web, daemon=True).start()

    # Bot 主執行
    run_bot()
