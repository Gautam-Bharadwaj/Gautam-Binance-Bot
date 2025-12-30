🚀 Binance Futures Order Bot (CLI-Based)

A CLI-based trading bot for Binance USDT-M Futures that supports basic and advanced order types, with robust validation, structured logging, and modular design.

This project is built for educational and evaluation purposes, focusing on clean architecture, safety, and real-world trading logic rather than profit generation.

📌 Features
✅ Core Orders (Mandatory)

Market Orders

Limit Orders

⭐ Advanced Orders (Bonus)

Stop-Limit Orders

OCO (One-Cancels-the-Other) – simulated for Futures

TWAP (Time-Weighted Average Price) – split orders over time

🔒 Safety & Engineering

Input validation before API calls

Centralized logging (bot.log)

Defensive programming for Binance Futures testnet limitations

CLI-based execution

Modular and extensible structure

🛠 Tech Stack

Language: Python 3

Binance API: python-binance

Environment Variables: python-dotenv

Logging: Python logging

CLI Handling: sys.argv

📂 Project Structure
Gautam-Binance-Bot/
│
├── src/
│   ├── config.py            # Binance client configuration
│   ├── logger.py            # Centralized logging
│   ├── validator.py         # Input validation
│   ├── market_orders.py     # Market orders
│   ├── limit_orders.py      # Limit orders
│   └── advanced/
│       ├── stop_limit.py    # Stop-Limit orders
│       ├── twap.py          # TWAP strategy
│       └── oco.py           # Simulated OCO orders
│
├── README.md
├── report.pdf
└── bot.log                  # Generated at runtime

🔑 API Setup

Create a Binance Futures TESTNET account
👉 https://testnet.binancefuture.com

Create a .env file in the project root:

BINANCE_API_KEY=your_api_key_here
BINANCE_API_SECRET=your_api_secret_here
BINANCE_TESTNET=true


⚠️ Never commit .env or bot.log to GitHub

📦 Installation
pip3 install python-binance python-dotenv

▶️ How to Run the Bot

All commands must be run from the project root directory.

🔹 Market Order
python3 -m src.market_orders BTCUSDT BUY 0.01

🔹 Limit Order
python3 -m src.limit_orders BTCUSDT SELL 0.01 45000

🔹 Stop-Limit Order
python3 -m src.advanced.stop_limit BTCUSDT SELL 0.01 44800 44700

🔹 TWAP Strategy
python3 -m src.advanced.twap BTCUSDT BUY 0.02 4 15


Total Quantity: 0.02

Number of slices: 4

Interval: 15 seconds

🔹 OCO (Simulated)
python3 -m src.advanced.oco BTCUSDT SELL 0.01 45500 44500


Places a take-profit and stop-loss order.
When one is filled, the other is cancelled.

📄 Logging

All actions are logged in bot.log, including:

Order placement

Validation errors

API responses

Testnet limitations

Execution status

Example log entry:

2025-12-30 | INFO | binance_bot | Placing MARKET order | Symbol: BTCUSDT | Side: BUY | Quantity: 0.01

⚠️ Known Limitations (Important)

Binance Futures TESTNET may return incomplete responses (e.g., missing orderId) for:

LIMIT orders

STOP orders

Conditional orders

This project detects and handles such cases gracefully instead of assuming successful execution.

This behavior is logged clearly and explained in report.pdf.

📘 Report

Please refer to report.pdf for:

Architecture overview

Order flow explanation

Screenshots of execution & logs

Discussion of testnet limitations

Design decisions

🔮 Future Improvements

WebSocket-based order monitoring

Native OCO support (spot)

Risk management rules

Strategy backtesting

Dashboard UI

🧑‍💻 Author

Kumar Gautam 
Binance Futures Order Bot – CLI
Academic / Learning Project

📌 Disclaimer

This project is for educational purposes only.
It is not financial advice and should not be used for live trading without proper risk management.