import sys
import time

from src.config import get_binance_client
from src.validator import (
    validate_symbol,
    validate_side,
    validate_quantity,
    validate_price,
)
from src.logger import setup_logger

logger = setup_logger()


def place_oco_order(
    symbol: str,
    side: str,
    quantity: float,
    take_profit_price: float,
    stop_loss_price: float,
):
    """
    Simulates an OCO (One-Cancels-the-Other) order on Binance Futures
    using a Take-Profit and a Stop-Loss order.
    """
    try:
        # ---------------- VALIDATION ----------------
        validate_symbol(symbol)
        validate_side(side)
        validate_quantity(quantity)
        validate_price(take_profit_price)
        validate_price(stop_loss_price)

        # Logical validation
        if side == "SELL" and not (take_profit_price > stop_loss_price):
            raise ValueError(
                "For SELL OCO, take-profit price must be higher than stop-loss price"
            )

        if side == "BUY" and not (take_profit_price < stop_loss_price):
            raise ValueError(
                "For BUY OCO, take-profit price must be lower than stop-loss price"
            )

        client = get_binance_client()

        logger.info(
            f"Placing OCO (simulated) | Symbol: {symbol} | Side: {side} | "
            f"Quantity: {quantity} | TP: {take_profit_price} | SL: {stop_loss_price}"
        )

        # ---------------- TAKE PROFIT ORDER ----------------
        tp_order = client.futures_create_order(
            symbol=symbol,
            side=side,
            type="LIMIT",
            timeInForce="GTC",
            quantity=quantity,
            price=take_profit_price,
        )

        if not tp_order or "orderId" not in tp_order:
            raise RuntimeError(
                "Take-profit order response missing orderId (testnet limitation)"
            )

        tp_order_id = tp_order["orderId"]
        logger.info(f"Take-profit order placed successfully: {tp_order}")

        # ---------------- STOP LOSS ORDER ----------------
        sl_order = client.futures_create_order(
            symbol=symbol,
            side=side,
            type="STOP",
            timeInForce="GTC",
            quantity=quantity,
            price=stop_loss_price,
            stopPrice=stop_loss_price,
        )

        if not sl_order or "orderId" not in sl_order:
            raise RuntimeError(
                "Stop-loss order response missing orderId (testnet limitation)"
            )

        sl_order_id = sl_order["orderId"]
        logger.info(f"Stop-loss order placed successfully: {sl_order}")

        # ---------------- MONITOR ORDERS ----------------
        logger.info("Monitoring OCO orders...")

        while True:
            tp_status = client.futures_get_order(
                symbol=symbol, orderId=tp_order_id
            )["status"]

            sl_status = client.futures_get_order(
                symbol=symbol, orderId=sl_order_id
            )["status"]

            if tp_status == "FILLED":
                logger.info(
                    "Take-profit order filled. Cancelling stop-loss order."
                )
                client.futures_cancel_order(
                    symbol=symbol, orderId=sl_order_id
                )
                break

            if sl_status == "FILLED":
                logger.info(
                    "Stop-loss order filled. Cancelling take-profit order."
                )
                client.futures_cancel_order(
                    symbol=symbol, orderId=tp_order_id
                )
                break

            time.sleep(5)

        logger.info("OCO execution completed successfully")
        print("✅ OCO order completed successfully")

    except Exception as e:
        logger.error(f"OCO execution failed: {str(e)}")
        print("❌ OCO execution failed. Check bot.log for details.")


def main():
    if len(sys.argv) != 6:
        print(
            "Usage: python3 -m src.advanced.oco "
            "<symbol> <BUY/SELL> <quantity> <take_profit_price> <stop_loss_price>"
        )
        sys.exit(1)

    symbol = sys.argv[1].upper()
    side = sys.argv[2].upper()
    quantity = float(sys.argv[3])
    take_profit_price = float(sys.argv[4])
    stop_loss_price = float(sys.argv[5])

    place_oco_order(
        symbol,
        side,
        quantity,
        take_profit_price,
        stop_loss_price,
    )


if __name__ == "__main__":
    main()
