import argparse
import os
import sys
from dotenv import load_dotenv
from bot.logging_config import setup_logging
from bot.validators import validate_inputs
from bot.client import BinanceFuturesTestnetClient
from bot.orders import OrderManager

load_dotenv()

def main():
    setup_logging()
    
    parser = argparse.ArgumentParser(description="Binance Futures Testnet Trading Bot CLI")
    parser.add_argument("--symbol", required=True, help="Trading pair (e.g., BTCUSDT)")
    parser.add_argument("--side", required=True, choices=["BUY", "SELL"], help="Order side")
    parser.add_argument("--type", required=True, choices=["MARKET", "LIMIT", "STOP_LIMIT"], help="Order type")
    parser.add_argument("--quantity", required=True, type=float, help="Order quantity")
    parser.add_argument("--price", type=float, help="Price (Required for LIMIT and STOP_LIMIT orders)")
    parser.add_argument("--stop_price", type=float, help="Stop Price (Required for STOP_LIMIT orders)")

    args = parser.parse_args()

    try:
        validate_inputs(args)
    except argparse.ArgumentError as e:
        print(f"Validation Error: {e.message}")
        sys.exit(1)

    api_key = os.getenv("BINANCE_API_KEY")
    api_secret = os.getenv("BINANCE_API_SECRET")

    if not api_key or not api_secret or "your_testnet" in api_key:
        print("Error: Please set your valid BINANCE_API_KEY and BINANCE_API_SECRET inside the .env file.")
        sys.exit(1)

    client = BinanceFuturesTestnetClient(api_key, api_secret)
    manager = OrderManager(client)
    
    print("\n--- Order Request Summary ---")
    print(f"Symbol:     {args.symbol.upper()}")
    print(f"Side:       {args.side.upper()}")
    print(f"Type:       {args.type.upper()}")
    print(f"Quantity:   {args.quantity}")
    if args.price:
        print(f"Price:      {args.price}")
    if args.stop_price:
        print(f"Stop Price: {args.stop_price}")
    print("-----------------------------\n")

    result = manager.execute(args)

    if result["success"]:
        data = result["data"]
        print("Execution Status: SUCCESS")
        print(f"Order ID:         {data.get('orderId')}")
        print(f"Status:           {data.get('status')}")
        print(f"Executed Qty:     {data.get('executedQty')}")
        print(f"Avg Price:        {data.get('avgPrice', 'N/A')}")
    else:
        print("Execution Status: FAILED")
        print(f"Error Details:    {result['error']}")

if __name__ == "__main__":
    main()