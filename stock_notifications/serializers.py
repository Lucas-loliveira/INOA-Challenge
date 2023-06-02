from rest_framework import serializers

from stocks.models import Stock

from .models import StockNotification


class StockNotificationSerializer(serializers.ModelSerializer):
    stock = serializers.CharField()

    class Meta:
        model = StockNotification
        exclude = ("last_notification",)
