import logging

from django.conf import settings

from stocks.models import Stock

from .brapi_api_client import BrapiAPIClient

logger = logging.getLogger(__name__)


class StocksImporter:
    def __init__(self) -> None:
        self.brapi_api_client = BrapiAPIClient()

    def import_stocks(self):
        logger.info("Importing stocks...")
        stocks_response = self.brapi_api_client.get_stocks()

        if not stocks_response or not stocks_response.ok:
            logger.error("Failed to retrieve stocks.")
            return False

        data = stocks_response.json()
        for item in data["stocks"]:
            self.save_stock(item)

        logger.info("Stock import completed successfully.")
        return True

    def save_stock(self, stock_data):
        if not stock_data.get("stock", False):
            logger.error("Invalid stock data: %s", stock_data)
            return False

        stock = stock_data["stock"]
        name = stock_data.get("name", stock_data["stock"])
        close = stock_data.get("close", 0)

        quote, _ = Stock.objects.get_or_create(stock=stock)
        quote.name = name
        quote.close = close
        quote.save()
        return True
