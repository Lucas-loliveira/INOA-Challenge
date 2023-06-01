from django.apps import AppConfig


class StocksConfig(AppConfig):
    import src.celeryy

    default_auto_field = "django.db.models.BigAutoField"
    name = "stocks"
