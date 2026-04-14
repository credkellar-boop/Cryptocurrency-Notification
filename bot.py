
"""Module for Noti_Fy_Crypto_Bot Telegram interface."""
import os
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CallbackQueryHandler, CommandHandler
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

async def send_transaction_alert(context, tx_data):
    """Sends an interactive transaction alert to Telegram."""
    chat_id = os.getenv('TELEGRAM_CHAT_ID')
    text = (
        f"⚠️ *New Transaction Detected*\n"
        f"Type: {tx_data['type']}\n"
        f"Amount: {tx_data['amount']} ETH\n"
        f"Action Required:"
    )

    keyboard = [
        [
            InlineKeyboardButton("✅ Approve", callback_data="tx_approve"),
            InlineKeyboardButton("❌ Deny", callback_data="tx_deny")
        ]
    ]
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    await context.bot.send_message(chat_id=chat_id, text=text, reply_markup=reply_markup, parse_mode='Markdown')

async def button_callback(update, context):
    """Handles the Approve/Deny button presses."""
    query = update.callback_query
    await query.answer()

    if query.data == "tx_approve":
        await query.edit_message_text(text="✅ *Transaction Approved*", parse_mode='Markdown')
    elif query.data == "tx_deny":
        await query.edit_message_text(text="❌ *Transaction Denied*", parse_mode='Markdown')

def main():
    """Initialize and start the bot."""
    TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
    
    # Build the application
    app = Application.builder().token(TOKEN).build()

    # Add handler for button clicks
    app.add_handler(CallbackQueryHandler(button_callback))

    print("Bot is polling...")
    app.run_polling()

if __name__ == "__main__":
    main()
