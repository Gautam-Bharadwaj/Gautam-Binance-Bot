import sys
from config import get_binance_client
from validator import validate_symbol, validate_side, validate_quantity
from logger import setup_logger

logger = setup_logger()


def place_market_order(symbol: str, side: str, quantity: float):
    """
    Places a market order on Binance USDT-M Futures
    """
    try:
        # Validate inputs
        validate_symbol(symbol)
        validate_side(side)
        validate_quantity(quantity)

        client = get_binance_client()

        logger.info(
            f"Placing MARKET order | Symbol: {symbol} | Side: {side} | Quantity: {quantity}"
        )

        order = client.futures_create_order(
            symbol=symbol,
            side=side,
            type="MARKET",
            quantity=quantity,
        )

        logger.info(f"Market order executed successfully: {order}")
        print("✅ Market order placed successfully")

    except Exception as e:
        logger.error(f"Market order failed: {str(e)}")
        print("❌ Failed to place market order. Check bot.log for details.")


def main():
    if len(sys.argv) != 4:
        print("Usage: python3 market_orders.py <symbol> <BUY/SELL> <quantity>")
        sys.exit(1)

    symbol = sys.argv[1].upper()
    side = sys.argv[2].upper()
    quantity = float(sys.argv[3])

    place_market_order(symbol, side, quantity)


if __name__ == "__main__":
    main()
