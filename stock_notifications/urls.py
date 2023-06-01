from django.urls import include, path
from rest_framework import routers

from .views import StockNotificationViewSet

router = routers.DefaultRouter()
router.register(r"stock-notifications", StockNotificationViewSet)

urlpatterns = [
    path("", include(router.urls)),
]
