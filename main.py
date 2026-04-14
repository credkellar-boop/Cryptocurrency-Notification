
import os
import asyncio
from web3 import Web3
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

# Load environment variables
load_dotenv()

# Configuration
WEB3_PROVIDER_URL = os.getenv("WEB3_PROVIDER_URL")
TOKEN = os.getenv("TELEGRAM_TOKEN")
AUTHORIZED_USER_ID = int(os.getenv("AUTHORIZED_USER_ID", 0))
WALLET_TO_WATCH = os.getenv("MONITORED_WALLET_ADDRESS")

# Initialize Web3
w3 = Web3(Web3.HTTPProvider(WEB3_PROVIDER_URL))

# Global state control
is_active = True

async def send_notification(application, tx):
    """Formats and sends the transaction alert."""
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

async def monitor_transactions(application):
    """Background task to monitor the blockchain."""
    global is_active
    print(f"Monitoring wallet: {WALLET_TO_WATCH}")
    last_block = w3.eth.block_number

    while True:
        try:
            if not is_active:
                await asyncio.sleep(5)
                continue

            current_block = w3.eth.block_number
            if current_block > last_block:
                for block_num in range(last_block + 1, current_block + 1):
                    block = w3.eth.get_block(block_num, full_transactions=True)
                    for tx in block.transactions:
                        if tx['to'] == WALLET_TO_WATCH or tx['from'] == WALLET_TO_WATCH:
                            await send_notification(application, tx)
                
                last_block = current_block
            
            await asyncio.sleep(10)
        except Exception as e:
            print(f"Error: {e}")
            await asyncio.sleep(10)

# --- Command Handlers ---

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id == AUTHORIZED_USER_ID:
        await update.message.reply_text("Noti_Fy Crypto Bot is active.")

async def status(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id == AUTHORIZED_USER_ID:
        state = "ONLINE" if is_active else "OFFLINE/PAUSED"
        await update.message.reply_text(f"System Status: {state} | Monitoring Active")

async def pause_bot(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global is_active
    if update.effective_user.id == AUTHORIZED_USER_ID:
        is_active = False
        await update.message.reply_text("Monitoring PAUSED. Alerts are offline.")

async def resume_bot(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global is_active
    if update.effective_user.id == AUTHORIZED_USER_ID:
        is_active = True
        await update.message.reply_text("Monitoring ONLINE. Scanning blocks...")

async def kill_bot(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id == AUTHORIZED_USER_ID:
        await update.message.reply_text("Shutting down bot process...")
        os._exit(0)

if __name__ == "__main__":
    application = ApplicationBuilder().token(TOKEN).build()

    # Mapping your requested commands
    application.add_handler(CommandHandler('start', start))
    application.add_handler(CommandHandler('status', status))
    application.add_handler(CommandHandler('online', resume_bot))
    application.add_handler(CommandHandler('offline', pause_bot))
    application.add_handler(CommandHandler('pause', pause_bot))
    application.add_handler(CommandHandler('stop', pause_bot))
    application.add_handler(CommandHandler('kill', kill_bot))

    loop = asyncio.get_event_loop()
    loop.create_task(monitor_transactions(application))

    print("Bot starting...")
    application.run_polling()
