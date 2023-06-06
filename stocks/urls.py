from django.urls import include, path
from rest_framework import routers

from stocks.views import StockViewSet

router = routers.SimpleRouter()
router.register(r"stocks", StockViewSet, basename="stock")

urlpatterns = [
    path("", include(router.urls)),
]
