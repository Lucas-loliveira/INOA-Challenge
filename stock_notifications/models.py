from django.db import models

from stocks.models import Stock


class StockNotification(models.Model):
    user = models.ForeignKey("auth.User", on_delete=models.CASCADE, default=1)
    stock = models.ForeignKey(Stock, on_delete=models.CASCADE)
    max_value = models.DecimalField(max_digits=10, decimal_places=2)
    min_value = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.user.username} - {self.stock.name}"

    class Meta:
        unique_together = (
            "user",
            "stock",
        )
