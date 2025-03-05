import sys
sys.stdout.reconfigure(encoding='utf-8')  # Configure stdout to support UTF-8 encoding for Persian output

from tronpy import Tron  # Import Tron class for interacting with the TRON blockchain
from tronpy.keys import PrivateKey  # Import PrivateKey class for signing transactions
from tronpy.providers import HTTPProvider  # Import HTTPProvider to connect to TRON nodes with an API key
import time  # Import time module for adding delays
import requests  # Import requests module for sending Telegram messages
from dotenv import load_dotenv  # Import load_dotenv to load environment variables from .env file
import os  # Import os module to access environment variables

# Load environment variables from .env file
load_dotenv()
PRIVATE_KEY = os.getenv("PRIVATE_KEY")  # Private key of the wallet to monitor and drain
WALLET_ADDRESS = os.getenv("WALLET_ADDRESS")  # Address of the wallet to monitor (source)
SAFE_WALLET = os.getenv("SAFE_WALLET")  # Address of the safe wallet to transfer TRX to (destination)
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")  # Telegram bot token for sending notifications
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")  # Telegram chat ID for receiving notifications
API_KEY = os.getenv("TRONGRID_API_KEY")  # TronGrid API key for accessing the TRON network

# Set up connection to the TRON mainnet using TronGrid API key
provider = HTTPProvider(api_key=API_KEY)  # Create an HTTP provider with the API key
client = Tron(provider=provider, network='mainnet')  # Initialize Tron client for mainnet
priv_key = PrivateKey(bytes.fromhex(PRIVATE_KEY))  # Convert private key from hex string to PrivateKey object

# Function to send notification messages to Telegram
def send_telegram_message(message):
    """
    Sends a message to a specified Telegram chat using the bot API.
    
    Args:
        message (str): The message to send to Telegram.
    """
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"  # Telegram API endpoint
    payload = {"chat_id": TELEGRAM_CHAT_ID, "text": message}  # Payload with chat ID and message
    try:
        requests.post(url, json=payload)  # Send the POST request to Telegram
    except Exception as e:
        print(f"Error sending Telegram message: {e}")  # Log any errors during message sending

# Fixed fee for TRX transactions (in TRX)
FIXED_FEE = 0.001  # Set a fixed transaction fee of 0.001 TRX (1000 sun)

# Main function to monitor and drain TRX from the wallet
def monitor_and_drain():
    """
    Monitors the wallet for new TRX deposits and transfers them to a safe wallet.
    Handles cases where the wallet address is not yet active on-chain.
    """
    last_balance = 0  # Default balance if the address is not found on-chain
    try:
        # Attempt to get the initial balance of the wallet
        last_balance = client.get_account_balance(WALLET_ADDRESS)
        send_telegram_message(f"Bot started - Initial balance: {last_balance} TRX")
        print(f"Initial balance: {last_balance} TRX")
    except Exception as e:
        # If the address is not found or there's an error, notify and proceed
        send_telegram_message(f"Address not yet active: {e}")
        print(f"Address not yet active: {e}")

    # Infinite loop to continuously monitor the wallet
    while True:
        try:
            # Get the current balance of the wallet
            current_balance = client.get_account_balance(WALLET_ADDRESS)
            if current_balance > last_balance:  # Check if new TRX has been deposited
                amount_received = current_balance - last_balance  # Calculate the received amount
                message = f"New deposit: {amount_received} TRX"
                print(message)
                send_telegram_message(message)
                
                amount_to_send = current_balance - FIXED_FEE  # Calculate amount to transfer after fee
                
                if amount_to_send > 0:  # Ensure there's enough TRX to send after the fee
                    try:
                        # Build and sign a transaction to transfer TRX to the safe wallet
                        txn = (
                            client.trx.transfer(WALLET_ADDRESS, SAFE_WALLET, int(amount_to_send * 1_000_000))  # Convert TRX to sun (1 TRX = 1,000,000 sun)
                            .build()  # Build the transaction
                            .sign(priv_key)  # Sign it with the private key
                        )
                        result = txn.broadcast()  # Broadcast the transaction to the network
                        success_message = f"Transaction successful - TXID: {result['txid']}\nAmount transferred: {amount_to_send} TRX\nFee: {FIXED_FEE} TRX"
                        print(success_message)
                        send_telegram_message(success_message)
                        last_balance = current_balance - amount_to_send  # Update last balance
                    except Exception as e:
                        # Handle any errors during the transaction
                        error_message = f"Error in transfer: {e}"
                        print(error_message)
                        send_telegram_message(error_message)
                else:
                    # Notify if the balance is insufficient after accounting for the fee
                    no_funds_message = "Insufficient balance after fee!"
                    print(no_funds_message)
                    send_telegram_message(no_funds_message)
            time.sleep(5)  # Wait 5 seconds before the next check
        except Exception as e:
            # Handle errors during balance checking (e.g., address not found)
            print(f"Error checking balance: {e}")
            send_telegram_message(f"Error checking balance: {e}")
            time.sleep(5)  # Wait and retry after an error

# Entry point of the script
if __name__ == "__main__":
    print("Bot started running...")
    monitor_and_drain()  # Start the monitoring and draining process