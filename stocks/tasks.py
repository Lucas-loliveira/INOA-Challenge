import requests
from celery import shared_task
from celery.utils.log import get_task_logger
from django.conf import settings
from django.utils import timezone

from .stocks_service.stocks_importer import StocksImporter

logger = get_task_logger(__name__)


@shared_task(name="task_get_stocks")
def task_get_stocks():
    stocks_importer = StocksImporter()
    stocks_importer.import_stocks()
    return True
