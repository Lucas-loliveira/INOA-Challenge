import logging

from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone

from .models import Stock
from .notifications.stock_notification import StockNotificationSender


@receiver(post_save, sender=Stock)
def check_stock_notification(sender, instance, created, **kwargs):
    send_notifications = StockNotificationSender()
    send_notifications.send_notifications(instance)
