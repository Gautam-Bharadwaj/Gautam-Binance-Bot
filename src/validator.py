from logger import setup_logger

logger = setup_logger()


def validate_symbol(symbol: str):
    if not symbol or not symbol.isalnum():
        logger.error(f"Invalid symbol provided: {symbol}")
        raise ValueError("Invalid trading symbol")


def validate_side(side: str):
    if side not in ["BUY", "SELL"]:
        logger.error(f"Invalid order side: {side}")
        raise ValueError("Order side must be BUY or SELL")


def validate_quantity(quantity: float):
    if quantity <= 0:
        logger.error(f"Invalid quantity: {quantity}")
        raise ValueError("Quantity must be greater than 0")


def validate_price(price: float):
    if price <= 0:
        logger.error(f"Invalid price: {price}")
        raise ValueError("Price must be greater than 0")


def validate_stop_price(stop_price: float, price: float, side: str):
    if stop_price <= 0:
        logger.error(f"Invalid stop price: {stop_price}")
        raise ValueError("Stop price must be greater than 0")

    if side == "BUY" and stop_price < price:
        raise ValueError("For BUY orders, stop price must be >= price")

    if side == "SELL" and stop_price > price:
        raise ValueError("For SELL orders, stop price must be <= price")

