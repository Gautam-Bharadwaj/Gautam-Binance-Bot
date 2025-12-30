import sys
import time

from src.config import get_binance_client
from src.validator import (
    validate_symbol,
    validate_side,
    validate_quantity,
)
from src.logger import setup_logger

logger = setup_logger()


def place_twap_order(
    symbol: str,
    side: str,
    total_quantity: float,
    num_slices: int,
    interval_seconds: int,
):
    """
    Executes a TWAP strategy by splitting a large order
    into smaller market orders over time.
    """
    try:
        # Basic validation
        validate_symbol(symbol)
        validate_side(side)
        validate_quantity(total_quantity)

        if num_slices <= 0:
            raise ValueError("Number of slices must be greater than 0")

        if interval_seconds <= 0:
            raise ValueError("Interval seconds must be greater than 0")

        client = get_binance_client()

        slice_quantity = round(total_quantity / num_slices, 8)

        logger.info(
            f"Starting TWAP | Symbol: {symbol} | Side: {side} | "
            f"Total Qty: {total_quantity} | Slices: {num_slices} | "
            f"Interval: {interval_seconds}s"
        )

        for i in range(1, num_slices + 1):
            logger.info(
                f"TWAP slice {i}/{num_slices} | "
                f"Placing market order of qty {slice_quantity}"
            )

            order = client.futures_create_order(
                symbol=symbol,
                side=side,
                type="MARKET",
                quantity=slice_quantity,
            )

            logger.info(f"TWAP slice {i} executed: {order}")

            if i < num_slices:
                time.sleep(interval_seconds)

        logger.info("TWAP execution completed successfully")
        print("✅ TWAP order completed successfully")

    except Exception as e:
        logger.error(f"TWAP execution failed: {str(e)}")
        print("❌ TWAP execution failed. Check bot.log for details.")


def main():
    if len(sys.argv) != 6:
        print(
            "Usage: python3 -m src.advanced.twap "
            "<symbol> <BUY/SELL> <total_quantity> <num_slices> <interval_seconds>"
        )
        sys.exit(1)

    symbol = sys.argv[1].upper()
    side = sys.argv[2].upper()
    total_quantity = float(sys.argv[3])
    num_slices = int(sys.argv[4])
    interval_seconds = int(sys.argv[5])

    place_twap_order(
        symbol,
        side,
        total_quantity,
        num_slices,
        interval_seconds,
    )


if __name__ == "__main__":
    main()
