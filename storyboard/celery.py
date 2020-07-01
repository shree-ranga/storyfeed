from __future__ import absolute_import
import os
from celery import Celery

if os.getenv("DJANGO_ENV") == "DEV":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "storyboard.settings.dev")
elif os.getenv("DJANGO_ENV") == "PROD":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "storyboard.settings.prod")

celery_app = Celery("storyboard")
celery_app.config_from_object("django.conf:settings", namespace="CELERY")
celery_app.autodiscover_tasks()
