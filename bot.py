
import os
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import Application, CallbackQueryHandler, ContextTypes
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

async def send_transaction_alert(context: ContextTypes.DEFAULT_TYPE, tx_data):
    """
    Sends an interactive transaction alert to Telegram.
    """
    chat_id = os.getenv('TELEGRAM_CHAT_ID')
    text = (
        f"🚨 *New Transaction Detected*\n"
        f"Type: {tx_data['type']}\n"
        f"Amount: {tx_data['amount']} ETH\n"
        f"Action Required:"
    )

    keyboard = [
        [
            InlineKeyboardButton("✅ Approve", callback_data="tx_approve"),
            InlineKeyboardButton("❌ Deny", callback_data="tx_deny"),
        ]
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)
    await context.bot.send_message(
        chat_id=chat_id, 
        text=text, 
        reply_markup=reply_markup, 
        parse_mode='Markdown'
    )

async def button_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Handles the Approve/Deny button presses.
    """
    query = update.callback_query
    await query.answer()

    if query.data == "tx_approve":
        await query.edit_message_text(text="✅ Transaction Approved.")
    else:
        await query.edit_message_text(text="❌ Transaction Denied.")

def main():
    """
    Starts the bot.
    """
    token = os.getenv('TELEGRAM_BOT_TOKEN')
    if not token:
        print("Error: TELEGRAM_BOT_TOKEN not found.")
        return

    # Create the Application
    app = Application.builder().token(token).build()

    # Add handler for button clicks
    app.add_handler(CallbackQueryHandler(button_callback))

    print("Bot is polling...")
    app.run_polling()

if __name__ == "__main__":
    main()
