
"""Module to purge sensitive data during an Emergency Lockdown"""
import os
import shutil

def purge_sensitive_data():
    # Define paths to sensitive temporary data
    # Add any specific log files or cache folders your bot creates
    paths_to_clear = [
        "__pycache__",           # Compiled Python files
        "session_logs.txt",      # Temporary transaction history
        ".web3_cache",           # Cached provider data
    ]

    print("Starting Security Wipe...")

    for path in paths_to_clear:
        try:
            if os.path.isfile(path):
                os.remove(path)
                print(f"Deleted file: {path}")
            elif os.path.isdir(path):
                shutil.rmtree(path)
                print(f"Purged directory: {path}")
        except Exception as e:
            print(f"Could not clear {path}: {e}")

    # Optional: Overwrite sensitive memory-mapped files here if necessary
    print("Security Wipe Complete. System is cold.")

if __name__ == "__main__":
    purge_sensitive_data()
