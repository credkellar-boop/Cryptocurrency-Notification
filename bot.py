
import os
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import Application, CallbackQueryHandler, ContextTypes
from dotenv import load_dotenv
from web3 import Web3

# Load variables
load_dotenv()

# Setup Web3 Connection
# Ensure 'WEB3_PROVIDER_URL' is set in your Railway variables
w3 = Web3(Web3.HTTPProvider(os.getenv('WEB3_PROVIDER_URL')))

async def button_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    if query.data == "tx_approve":
        await query.edit_message_text(text="✅ Transaction Approved.")
    else:
        await query.edit_message_text(text="❌ Transaction Denied.")

def main():
    # Changed from TELEGRAM_BOT_TOKEN to BOT_ID to match your Railway settings
    token = os.getenv('BOT_ID')
    
    if not token:
        print("Error: BOT_ID not found in environment.")
        return

    # Build the Application
    app = Application.builder().token(token).build()

    # Add handler for the interactive buttons
    app.add_handler(CallbackQueryHandler(button_callback))

    print("--- Noti_Fy_Crypto_Bot is Active ---")
    app.run_polling()

if __name__ == "__main__":
    main()
