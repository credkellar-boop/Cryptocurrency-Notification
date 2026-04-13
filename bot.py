""" Real-time blockchain transaction listener for crypto alerts. """
import os
from dotenv import load_dotenv
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import Application, CallbackQueryHandler, CommandHandler, ContextTypes

load_dotenv()

async def send_transaction_alert(context, tx_data):
    """Triggered when the listener detects a transaction."""
    chat_id = "YOUR_CHAT_ID" # You can get this by messaging your bot
    text = (f"🔔 *New Transaction Detected*\n\n"
            f"Type: {tx_data['type']}\n"
            f"Amount: {tx_data['amount']} ETH\n"
            f"To: {tx_data['to']}\n\n"
            f"Action Required:")
    
    keyboard = [
        [
            InlineKeyboardButton("✅ Approve", callback_id="tx_approve"),
            InlineKeyboardButton("❌ Deny", callback_id="tx_deny")
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await context.bot.send_message(chat_id=chat_id, text=text, reply_markup=reply_markup, parse_mode='Markdown')

async def button_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data == "tx_approve":
        # Insert Logic to sign and broadcast the transaction here
        await query.edit_message_text(text="✅ *Status: Transaction Approved and Signed.*", parse_mode='Markdown')
    else:
        await query.edit_message_text(text="❌ *Status: Transaction Denied and Cancelled.*", parse_mode='Markdown')

def main():
    app = Application.builder().token(os.getenv("TELEGRAM_BOT_TOKEN")).build()
    app.add_handler(CallbackQueryHandler(button_callback))
    print("Bot is running...")
    app.run_polling()

if __name__ == "__main__":
    main()
