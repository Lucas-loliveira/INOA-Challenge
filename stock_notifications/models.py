from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator
from django.db import models

from stocks.models import Stock


class StockNotification(models.Model):
    user = models.ForeignKey("auth.User", on_delete=models.CASCADE, default=1)
    stock = models.ForeignKey(Stock, on_delete=models.CASCADE)
    max_value = models.DecimalField(
        max_digits=10, decimal_places=2, validators=[MinValueValidator(0)]
    )
    min_value = models.DecimalField(
        max_digits=10, decimal_places=2, validators=[MinValueValidator(0)]
    )
    last_notification = models.DateTimeField(null=True, blank=True)
    notification_interval_min = models.IntegerField(null=True, blank=True, default=5)

    def __str__(self):
        return f"{self.user.username} - {self.stock.name}"

    def clean(self):
        if self.max_value < self.min_value:
            raise ValidationError(
                "Max value must be greater than or equal to min value."
            )

    class Meta:
        unique_together = (
            "user",
            "stock",
        )
