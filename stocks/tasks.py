import requests
from celery import shared_task
from celery.utils.log import get_task_logger
from django.conf import settings
from django.utils import timezone

from .models import Stock

logger = get_task_logger(__name__)


@shared_task(name="sample_task1")
def sample_task1():
    url = "https://brapi.dev/api/quote/list?sortBy=close&sortOrder=desc&limit=10000"
    response = requests.get(url)
    data = response.json()

    for item in data["stocks"]:
        stock = item["stock"]
        name = item.get("name", item["stock"])
        close = item.get("close", 0)
        quote, created = Stock.objects.get_or_create(stock=stock)
        quote.name = name
        quote.close = close
        quote.updated_at = timezone.now()
        quote.save()
    return True
