
import os
import asyncio
from web3 import Web3
from dotenv import load_dotenv
from telegram import Bot

load_dotenv()

# Setup Web3 and Telegram
w3 = Web3(Web3.HTTPProvider(os.getenv("WEB3_PROVIDER_URL")))
bot = Bot(token=os.getenv("TELEGRAM_BOT_TOKEN"))
wallet_to_watch = os.getenv("MONITORED_WALLET_ADDRESS")

async def monitor_transactions():
    print(f"Monitoring wallet: {wallet_to_watch}")
    # Get the latest block to start
    last_block = w3.eth.block_number

    while True:
        try:
            current_block = w3.eth.block_number
            if current_block > last_block:
                for block_num in range(last_block + 1, current_block + 1):
                    block = w3.eth.get_block(block_num, full_transactions=True)
                    for tx in block.transactions:
                        if tx['to'] == wallet_to_watch or tx['from'] == wallet_to_watch:
                            await send_notification(tx)
                last_block = current_block
            await asyncio.sleep(10) # Poll every 10 seconds
        except Exception as e:
            print(f"Error: {e}")

async def send_notification(tx):
    message = (
        f"🚨 *Transaction Detected!*\n\n"
        f"From: `{tx['from']}`\n"
        f"To: `{tx['to']}`\n"
        f"Value: {w3.from_wei(tx['value'], 'ether')} ETH\n"
        f"Hash: `{tx['hash'].hex()}`"
    )
    await bot.send_message(chat_id=os.getenv("AUTHORIZED_USER_ID"), text=message, parse_mode='Markdown')

if __name__ == "__main__":
    asyncio.run(monitor_transactions())
