import logging
from bot.client import BinanceFuturesTestnetClient

logger = logging.getLogger(__name__)

class OrderManager:
    def __init__(self, client: BinanceFuturesTestnetClient):
        self.client = client

    def execute(self, args):
        logger.info(f"Initiating execution for {args.symbol} {args.side} {args.type}")
        result = self.client.place_order(
            symbol=args.symbol,
            side=args.side,
            order_type=args.type,
            quantity=args.quantity,
            price=args.price,
            stop_price=args.stop_price
        )
        return result