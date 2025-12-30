import os
from dotenv import load_dotenv
from binance.client import Client
from logger import setup_logger

# Load environment variables
load_dotenv()

logger = setup_logger()

def get_binance_client():
    """
    Returns a Binance Futures client (Testnet or Live)
    """

    api_key = os.getenv("BINANCE_API_KEY")
    api_secret = os.getenv("BINANCE_API_SECRET")
    use_testnet = os.getenv("BINANCE_TESTNET", "true").lower() == "true"

    if not api_key or not api_secret:
        logger.error("API keys not found. Please set them in .env file.")
        raise ValueError("Missing Binance API credentials")

    client = Client(api_key, api_secret)

    if use_testnet:
        client.FUTURES_URL = "https://testnet.binancefuture.com"
        logger.info("Using Binance Futures TESTNET")
    else:
        logger.info("Using Binance Futures LIVE environment")

    return client

