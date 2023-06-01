import logging
import os

import requests
from requests.exceptions import ConnectionError

logger = logging.getLogger(__name__)


class BrapiAPIClient:
    def __init__(self) -> None:
        self.url = os.environ.get(
            "STOCKS_API_URL",
            "https://brapi.dev/api/quote/list?sortBy=close&sortOrder=desc&limit=10000",
        )

    def get_stocks(self):
        try:
            response = requests.get(self.url)
        except ConnectionError:
            return False

        return response
