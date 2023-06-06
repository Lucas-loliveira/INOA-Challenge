import logging
from datetime import timedelta

from django.conf import settings
from django.core.mail import send_mail
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone

from stock_notifications.models import StockNotification


class StockNotificationSender:
    def __init__(self):
        logger = logging.getLogger(__name__)
        logger.setLevel(logging.INFO)
        logger.handlers = []
        handler = logging.FileHandler("stock_emails.log")
        handler.setLevel(logging.INFO)
        formatter = logging.Formatter("%(asctime)s %(levelname)s %(message)s")
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        self.logger = logger

    def send_notifications(self, instance: StockNotification) -> None:
        notifications = StockNotification.objects.filter(stock=instance)
        current_stock_value = instance.close

        for notification in notifications:
            if notification.min_value < current_stock_value < notification.max_value:
                continue

            last_notification = notification.last_notification

            if self.check_notification_can_be_send(
                last_notification, notification.notification_interval_min
            ):
                if self.send_email_notification(notification, current_stock_value):
                    notification.last_notification = timezone.now()
                    notification.save()

    def check_notification_can_be_send(
        self, last_notification, notification_interval_min: int
    ) -> bool:
        if last_notification is None:
            return True

        interval_seconds = notification_interval_min * 60
        time_elapsed = timedelta.total_seconds(timezone.now() - last_notification)
        return time_elapsed >= interval_seconds

    def send_email_notification(
        self, notification: StockNotification, current_value: float
    ) -> bool:
        if current_value > notification.max_value:
            reference_value = notification.max_value
            advice = "VENDER"
            notification_type = "excedeu o valor máximo"
        elif current_value < notification.min_value:
            reference_value = notification.min_value
            advice = "COMPRAR"
            notification_type = "está abaixo do valor mínimo"
        else:
            return False

        subject = f"Notificação de Ação: {notification.stock.stock}"
        message = (
            f"Prezado(a) {notification.user.username},\n\n"
            f"A ação {notification.stock.stock} ({notification.stock.name}) {notification_type} "
            f"de {reference_value}. O valor atual é {current_value}.\n\n"
            f"Recomendação: {advice}\n"
            f"Obrigado por utilizar o nosso serviço de notificação de ações.\n"
        )

        send_mail(
            subject=subject,
            message=message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[notification.user.email],
        )

        self.logger.info(
            f"E-mail de notificação enviado para {notification.user.email} - {message}"
        )
        return True
