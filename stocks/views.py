from rest_framework import mixins, viewsets

from .models import Stock
from .serializers import StockSerializer


class StockViewSet(
    mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet
):
    queryset = Stock.objects.all()
    serializer_class = StockSerializer
