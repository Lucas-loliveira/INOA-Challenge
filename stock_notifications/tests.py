from django.contrib.auth.models import User
from rest_framework.test import APIClient, APITestCase

from .models import Stock, StockNotification


class StockNotificationAPITestCase(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username="testuser", password="testpass")
        self.stock = Stock.objects.create(stock="AAPL", name="Apple", close=100)
        self.valid_payload = {
            "stock": self.stock.stock,
            "max_value": 150.00,
            "min_value": 80.00,
        }

    def test_create_stock_notification(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.post(
            "/api/stock-notifications/", data=self.valid_payload
        )
        stock_notification = StockNotification.objects.get(
            user=self.user, stock=self.stock
        )

        self.assertEqual(response.status_code, 201)
        self.assertEqual(stock_notification.user, self.user)
        self.assertEqual(stock_notification.stock, self.stock)
        self.assertEqual(stock_notification.max_value, self.valid_payload["max_value"])
        self.assertEqual(stock_notification.min_value, self.valid_payload["min_value"])

    def test_create_stock_notification_invalid_stock(self):
        invalid_payload = {"stock": 9999, "max_value": 150.00, "min_value": 80.00}
        self.client.force_authenticate(user=self.user)

        response = self.client.post("/api/stock-notifications/", data=invalid_payload)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json()[0], "Specified stock does not exist.")

    def test_get_stock_notifications(self):
        StockNotification.objects.create(
            user=self.user, stock=self.stock, max_value=150.00, min_value=80.00
        )
        self.client.force_authenticate(user=self.user)
        response = self.client.get("/api/stock-notifications/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)
        stock_notification = response.json()[0]
        self.assertEqual(stock_notification["user"], self.user.id)
        self.assertEqual(stock_notification["stock"], self.stock.stock)
        self.assertEqual(stock_notification["max_value"], "150.00")
        self.assertEqual(stock_notification["min_value"], "80.00")

    def test_get_stock_notification_other_user(self):
        other_user = User.objects.create_user(username="otheruser", password="testpass")
        stock_notification = StockNotification.objects.create(
            user=other_user, stock=self.stock, max_value=150.00, min_value=80.00
        )

        self.client.force_authenticate(user=self.user)
        response = self.client.get(f"/api/stock-notifications/{stock_notification.id}/")

        self.assertEqual(response.status_code, 404)
