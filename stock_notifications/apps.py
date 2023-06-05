from django.apps import AppConfig


class StockNotificationsConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "stock_notifications"

    def ready(self):
        import stock_notifications.signals
