# Binance Futures Trading Bot

A Command Line Interface (CLI) application built in Python to execute trades on the Binance Futures Testnet.

## Features
* Supports BUY and SELL orders.
* Order types handled: MARKET, LIMIT, and STOP.
* Modular architecture with secure API key handling.

## Setup Instructions
1. Install requirements: `pip install -r requirements.txt`
2. Create a `.env` file and add your testnet keys:
   `BINANCE_API_KEY=your_key`
   `BINANCE_API_SECRET=your_secret`

## How to Run (Example)
`python cli.py --symbol BTCUSDT --side BUY --type STOP_LIMIT --quantity 0.05 --price 68000 --stop_price 68500`