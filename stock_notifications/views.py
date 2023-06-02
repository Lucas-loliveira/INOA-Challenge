from django.core.exceptions import ObjectDoesNotExist
from rest_framework import serializers, viewsets

from stocks.models import Stock

from .models import StockNotification
from .permissions import IsAuthenticatedAndOwner
from .serializers import StockNotificationSerializer


class StockNotificationViewSet(viewsets.ModelViewSet):
    queryset = StockNotification.objects.all()
    serializer_class = StockNotificationSerializer
    permission_classes = [IsAuthenticatedAndOwner]

    def get_stock_by_name(self, stock_name):
        try:
            stock = Stock.objects.get(stock=stock_name)
        except ObjectDoesNotExist:
            raise serializers.ValidationError("Specified stock does not exist.")
        return stock

    def perform_create(self, serializer):
        stock_name = self.request.data.get("stock")
        stock = self.get_stock_by_name(stock_name)
        serializer.save(user=self.request.user, stock=stock)

    def perform_update(self, serializer):
        stock_name = self.request.data.get("stock")
        stock = self.get_stock_by_name(stock_name)
        serializer.save(user=self.request.user, stock=stock)

    def get_queryset(self):
        user = self.request.user
        return StockNotification.objects.filter(user=user)
