from __future__ import absolute_import, unicode_literals

import os

from celery import Celery
from decouple import config

# Set the default Django settings module
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "src.settings")

app = Celery("src")
app.config_from_object("django.conf:settings", namespace="")

# Load task modules from all registered Django app configs
app.autodiscover_tasks()
