
import os
import time
from web3 import Web3
from dotenv import load_dotenv

# Load environment variables from your private .env file
load_dotenv()

def handle_event(transaction):
    """Processes detected blockchain transactions."""
    print(f"Transaction Found: {transaction['hash'].hex()}")

def log_loop(poll_interval):
    """Main loop to poll the blockchain for new blocks with auto-reconnect."""
    # 1. Establish the connection ONCE outside the loop for stability
    infura_url = os.getenv('INFURA_API_URL')
    target_address = os.getenv('0xE7512f65508306Dc669Ef232Bcb31A8Aacd73A37')
    
    w3 = Web3(Web3.HTTPProvider(infura_url))
    
    print(f"Monitoring address: {target_address}")

    while True:
        try:
            # Check if we are still connected
            if not w3.is_connected():
                print("Connection lost. Reconnecting...")
                w3 = Web3(Web3.HTTPProvider(infura_url))
            
            # 2. Get the latest block
            block = w3.eth.get_block('latest', full_transactions=True)
            
            for tx in block.transactions:
                # 3. Check both 'to' and 'from' so you see all activity
                if tx['to'] == target_address or tx['from'] == target_address:
                    handle_event(tx)
            
            time.sleep(poll_interval)

        except Exception as e:
            # 4. If any error happens (internet out, etc.), wait and retry
            print(f"Connection error: {e}. Retrying in 5 seconds...")
            time.sleep(5)

if __name__ == "__main__":
    # Standard 10-second poll to stay within Infura free-tier limits
    log_loop(10)
