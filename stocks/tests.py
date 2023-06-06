from unittest.mock import MagicMock, patch

from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from .models import Stock
from .serializers import StockSerializer
from .stocks_service.stocks_importer import StocksImporter


class StocksImporterTest(TestCase):
    @patch("stocks.stocks_service.stocks_importer.BrapiAPIClient.get_stocks")
    def test_import_stocks_success(self, mock_get_stocks):
        mock_response = MagicMock()
        mock_response.ok = True
        mock_response.json.return_value = {
            "stocks": [
                {"stock": "ABC", "name": "Stock ABC", "close": 10},
                {"stock": "DEF", "name": "Stock DEF", "close": 20},
            ]
        }
        mock_get_stocks.return_value = mock_response

        stocks_importer = StocksImporter()
        result = stocks_importer.import_stocks()

        self.assertTrue(result)

        stock_abc = Stock.objects.get(stock="ABC")
        self.assertEqual(stock_abc.name, "Stock ABC")
        self.assertEqual(stock_abc.close, 10)

        stock_def = Stock.objects.get(stock="DEF")
        self.assertEqual(stock_def.name, "Stock DEF")
        self.assertEqual(stock_def.close, 20)

    @patch("stocks.stocks_service.stocks_importer.BrapiAPIClient.get_stocks")
    def test_import_stocks_failure(self, mock_get_stocks):
        mock_response = MagicMock()
        mock_response.ok = False
        mock_get_stocks.return_value = mock_response

        stocks_importer = StocksImporter()
        result = stocks_importer.import_stocks()

        self.assertFalse(result)
        self.assertEqual(Stock.objects.count(), 0)


class StockAPITestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.stock1 = Stock.objects.create(stock="AAPL", name="Apple Inc.", close=150.0)
        self.stock2 = Stock.objects.create(
            stock="GOOGL", name="Alphabet Inc.", close=2500.0
        )

    def test_list_stocks(self):
        url = reverse("stock-list")
        response = self.client.get(url)
        stocks = Stock.objects.all()
        serializer = StockSerializer(stocks, many=True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def test_retrieve_stock(self):
        url = reverse("stock-detail", kwargs={"pk": self.stock1.pk})
        response = self.client.get(url)
        stock = Stock.objects.get(pk=self.stock1.pk)
        serializer = StockSerializer(stock)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)
