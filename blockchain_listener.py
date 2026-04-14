
"""Module for real-time blockchain transaction monitoring."""
import os
import time
from web3 import Web3
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def handle_event(transaction):
    """Processes detected blockchain transactions."""
    print(f"Transaction Found: {transaction['hash'].hex()}")

def log_loop(poll_interval):
    """Main loop to poll the blockchain for new blocks."""
    w3 = Web3(Web3.HTTPProvider(os.getenv('INFURA_URL')))
    target_address = os.getenv('WALLET_ADDRESS')

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

