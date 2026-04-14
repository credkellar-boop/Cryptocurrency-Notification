
import os
import asyncio
from web3 import Web3
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from dotenv import load_dotenv

load_dotenv()

# Setup Web3 and Telegram
w3 = Web3(Web3.HTTPProvider(os.getenv("WEB3_PROVIDER_URL")))
TOKEN = os.getenv("TELEGRAM_TOKEN")
AUTHORIZED_USER_ID = int(os.getenv("AUTHORIZED_USER_ID", 0))
wallet_to_watch = os.getenv("MONITORED_WALLET_ADDRESS")

async def monitor_transactions(application):
    print(f"Monitoring wallet: {wallet_to_watch}")
    last_block = w3.eth.block_number

    while True:
        try:
            current_block = w3.eth.block_number
            if current_block > last_block:
                for block_num in range(last_block + 1, current_block + 1):
                    block = w3.eth.get_block(block_num, full_transactions=True)
                    for tx in block.transactions:
                        if tx['to'] == wallet_to_watch or tx['from'] == wallet_to_watch:
                            message = (
                                f"🚨 *Transaction Detected!*\n\n"
                                f"*From:* `{tx['from']}`\n"
                                f"*To:* `{tx['to']}`\n"
                                f"*Value:* {w3.from_wei(tx['value'], 'ether')} ETH\n"
                                f"*Hash:* `{tx['hash'].hex()}`"
                            )
                            await application.bot.send_message(
                                chat_id=AUTHORIZED_USER_ID, 
                                text=message, 
                                parse_mode='Markdown'
                            )
                last_block = current_block
            await asyncio.sleep(10)
        except Exception as e:
            print(f"Error: {e}")
            await asyncio.sleep(10)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id == AUTHORIZED_USER_ID:
        await update.message.reply_text("Noti_Fy_Crypto_Bot is Active. Voice & Biometrics removed.")

async def status(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id == AUTHORIZED_USER_ID:
        await update.message.reply_text("System Status: Online | Monitoring Active")

if __name__ == "__main__":
    application = ApplicationBuilder().token(TOKEN).build()
    
    # Add Handlers
    application.add_handler(CommandHandler('start', start))
    application.add_handler(CommandHandler('status', status))

    # Start the bot and the monitor together
    loop = asyncio.get_event_loop()
    loop.create_task(monitor_transactions(application))
    
    print("Bot starting...")
    application.run_polling()
