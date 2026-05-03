import os
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, ContextTypes, filters

TOKEN = os.getenv("BOT_TOKEN")

GROUP_ID = -5105827693
ALLOWED_USERS = [1165688271]

# ===== bot 邏輯 =====
async def relay(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message:
        return

    user_id = update.message.from_user.id
    text = update.message.text

    print("收到訊息:", text, flush=True)

    if user_id not in ALLOWED_USERS:
        return

    await context.bot.send_message(chat_id=GROUP_ID, text=text)

def run_bot():
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, relay))

    print("Bot started", flush=True)
    app.run_polling()

if __name__ == "__main__":
    run_bot()
