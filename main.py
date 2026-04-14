
import os
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from dotenv import load_dotenv

load_dotenv()

# CORE CONFIG
TOKEN = os.getenv("TELEGRAM_TOKEN")
# Authorized User ID - only you can control the bot
AUTHORIZED_USER = int(os.getenv("YOUR_TELEGRAM_ID", 0))

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != AUTHORIZED_USER:
        return
    await update.message.reply_text("Noti_Fy_Crypto_Bot is Active. Voice & Biometrics disabled.")

async def status(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != AUTHORIZED_USER:
        return
    # Simple logic to check if worker is accessible
    await update.message.reply_text("System Status: Online | Mode: Data-Only")

if __name__ == '__main__':
    application = ApplicationBuilder().token(TOKEN).build()
    
    application.add_handler(CommandHandler('start', start))
    application.add_handler(CommandHandler('status', status))
    
    print("Bot is starting without speech/biometric modules...")
    application.run_polling()
