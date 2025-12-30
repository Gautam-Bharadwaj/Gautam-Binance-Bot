import sys
from config import get_binance_client
from validator import (
    validate_symbol,
    validate_side,
    validate_quantity,
    validate_price,
)
from logger import setup_logger

logger = setup_logger()


def place_limit_order(symbol: str, side: str, quantity: float, price: float):
    """
    Places a limit order on Binance USDT-M Futures
    """
    try:
        # Validate inputs
        validate_symbol(symbol)
        validate_side(side)
        validate_quantity(quantity)
        validate_price(price)

        client = get_binance_client()

        logger.info(
            f"Placing LIMIT order | Symbol: {symbol} | Side: {side} | "
            f"Quantity: {quantity} | Price: {price}"
        )

        order = client.futures_create_order(
            symbol=symbol,
            side=side,
            type="LIMIT",
            timeInForce="GTC",
            quantity=quantity,
            price=price,
        )

        logger.info(f"Limit order placed successfully: {order}")
        print("✅ Limit order placed successfully")

    except Exception as e:
        logger.error(f"Limit order failed: {str(e)}")
        print("❌ Failed to place limit order. Check bot.log for details.")


def main():
    if len(sys.argv) != 5:
        print(
            "Usage: python3 limit_orders.py <symbol> <BUY/SELL> <quantity> <price>"
        )
        sys.exit(1)

    symbol = sys.argv[1].upper()
    side = sys.argv[2].upper()
    quantity = float(sys.argv[3])
    price = float(sys.argv[4])

    place_limit_order(symbol, side, quantity, price)


if __name__ == "__main__":
    main()
