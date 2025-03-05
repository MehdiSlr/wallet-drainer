# TRON Wallet Drainer Bot

This is a Python script that monitors a TRON wallet for incoming TRX deposits and automatically transfers them to a specified safe wallet. It includes Telegram notifications for real-time updates and uses the TronGrid API for blockchain interaction. The bot is designed to run continuously and can be deployed on a server for 24/7 operation.

## Features

- Monitors a TRON wallet for new TRX deposits.

- Automatically transfers TRX to a safe wallet, accounting for a fixed transaction fee (0.001 TRX).

- Sends real-time notifications to Telegram for deposits, successful transfers, and errors.

- Handles inactive wallet addresses gracefully with error management.

- Configurable via environment variables for security.

# Prerequisites

- Python 3.8 or higher installed on your system.

- A TronGrid API key (get it from [TronGrid](https://www.trongrid.io/)).

- A Telegram bot and chat ID (create one via [BotFather](https://t.me/BotFather)).

- A TRON wallet private key and addresses (source and safe wallets).

## Installation

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/tron-wallet-drainer.git
cd tron-wallet-drainer
```

### 2. Install Dependencies Install the required Python packages listed in `requirements.txt`:

```bash
pip install -r requirements.txt
```

### 3. Set Up Environment Variables

- Copy the `env.example` file to `.env`:

```bash
cp env.example .env
```

- Edit `.env` with your own values:

```text
PRIVATE_KEY=your_private_key_here           # Your TRON wallet private key (e.g., 12244bd4c27a36a57da640511cb525ee4efg458hyu7892ijh063dfg454j87ioz)
WALLET_ADDRESS=your_wallet_address_here     # Source wallet to monitor (e.g., TSAMuW4vJeCT9zdfgERTY84Kghj23nKJum)
SAFE_WALLET=your_safe_wallet_address_here   # Destination wallet for TRX (e.g., TQ5XoPGrXtETaaakS5VFcKdQXjfQXvY9zm)
TELEGRAM_TOKEN=your_telegram_token_here     # Telegram bot token (e.g., 5698213645:ANHYgH_Hxzp-fgTrYJfgVNRNeQ08t9VF5TR)
TELEGRAM_CHAT_ID=your_telegram_chat_id_here # Telegram chat ID (e.g., 96547236)
TRONGRID_API_KEY=your_trongrid_api_key_here # TronGrid API key (e.g., rtn654ec-5628-95b3-ba20-afa493tph8sv)
```

## Usage

### 1. Run Locally Execute the script on your local machine:

```bash
python tron.py
```

- The bot will start monitoring the WALLET_ADDRESS for TRX deposits.

- If the address is inactive (no transactions yet), it will wait until TRX is deposited.

### 2. Test the Bot

- Send a small amount of TRX (e.g., 0.1 TRX) to WALLET_ADDRESS.

- Check your Telegram chat for notifications and the console for logs.

### 3. Deploy for 24/7 Operation To keep the bot running continuously, deploy it to a server:

- Render (Free):

    1. Sign up at Render.

    2. Create a new "Background Worker".

    3. Upload the repository and set the start command to python tron.py.

    4. Add environment variables from .env in the Render dashboard.

- Vultr VPS (Paid):

    1. Sign up at Vultr.

    2. Create a $5/month Ubuntu server.

    3. SSH into the server, upload files, install dependencies, and run:

```bash
nohup python tron.py &
```

## Files

- `tron.py`: Main script that monitors and drains TRX from the wallet.

- `env.example`: Template for environment variables.

- `requirements.txt`: List of Python dependencies.

## Notes

- Security: Never share your `.env` file or private key publicly. Store them securely.

- Wallet Activation: The `WALLET_ADDRESS` must have at least one transaction (e.g., a small TRX deposit) to be recognized on-chain.

- Fee: The bot uses a fixed fee of 0.001 TRX. Adjust `FIXED_FEE` in `tron.py` if network conditions change.

## Troubleshooting

- AddressNotFound Error: Ensure `WALLET_ADDRESS` is correct and active (has TRX or a past transaction).

- API Errors: Verify your `TRONGRID_API_KEY` is valid and not expired.

- Telegram Issues: Check `TELEGRAM_TOKEN` and `TELEGRAM_CHAT_ID` for accuracy.

## Contributing

Feel free to fork this repository, submit issues, or send pull requests with improvements!

## License
This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Acknowledgments
- Built with [tronpy](https://github.com/andelf/tronpy) for TRON blockchain interaction.

- Inspired by the need to automate wallet monitoring and transfers.
