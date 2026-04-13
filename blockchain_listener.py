""" Real-time blockchain transaction listener for crypto alerts. """
""" This module handles real-time cryptocurrency notifications. """
import time
from web3 import Web3
from dotenv import load_dotenv
import os

load_dotenv()
w3 = Web3(Web3.HTTPProvider(os.getenv("INFURA_API_URL")))
target_address = os.getenv("WALLET_ADDRESS").lower()

def handle_event(transaction):
    # This is where you would call the bot.py alert function
    print(f"Transaction Found: {transaction['hash'].hex()}")

def log_loop(poll_interval):
    print(f"Monitoring address: {target_address}")
    while True:
        # Check latest block
        block = w3.eth.get_block('latest', full_transactions=True)
        for tx in block.transactions:
            if tx['to'] == target_address or tx['from'] == target_address:
                handle_event(tx)
        time.sleep(poll_interval)

if __name__ == "__main__":
    log_loop(10)
