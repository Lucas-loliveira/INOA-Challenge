# Generated by Django 4.2.1 on 2023-06-01 19:52

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("stocks", "0002_alter_stock_close_alter_stock_created_at_and_more"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("stock_notifications", "0001_initial"),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name="stocknotification",
            unique_together={("user", "stock")},
        ),
    ]