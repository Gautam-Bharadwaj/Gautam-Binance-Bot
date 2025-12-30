import sys
from src.config import get_binance_client
from src.validator import (
    validate_symbol,
    validate_side,
    validate_quantity,
    validate_price,
    validate_stop_price,
)
from src.logger import setup_logger


logger = setup_logger()


def place_stop_limit_order(
    symbol: str,
    side: str,
    quantity: float,
    limit_price: float,
    stop_price: float,
):
    """
    Places a STOP-LIMIT order on Binance USDT-M Futures
    """
    try:
        # Validate inputs
        validate_symbol(symbol)
        validate_side(side)
        validate_quantity(quantity)
        validate_price(limit_price)
        validate_stop_price(stop_price, limit_price, side)

        client = get_binance_client()

        logger.info(
            f"Placing STOP-LIMIT order | Symbol: {symbol} | Side: {side} | "
            f"Quantity: {quantity} | Limit: {limit_price} | Stop: {stop_price}"
        )

        order = client.futures_create_order(
            symbol=symbol,
            side=side,
            type="STOP",
            timeInForce="GTC",
            quantity=quantity,
            price=limit_price,
            stopPrice=stop_price,
        )

        logger.info(f"Stop-Limit order placed successfully: {order}")
        print("✅ Stop-Limit order placed successfully")

    except Exception as e:
        logger.error(f"Stop-Limit order failed: {str(e)}")
        print("❌ Failed to place stop-limit order. Check bot.log for details.")


def main():
    if len(sys.argv) != 6:
        print(
            "Usage: python3 stop_limit.py <symbol> <BUY/SELL> <quantity> <limit_price> <stop_price>"
        )
        sys.exit(1)

    symbol = sys.argv[1].upper()
    side = sys.argv[2].upper()
    quantity = float(sys.argv[3])
    limit_price = float(sys.argv[4])
    stop_price = float(sys.argv[5])

    place_stop_limit_order(symbol, side, quantity, limit_price, stop_price)


if __name__ == "__main__":
    main()
