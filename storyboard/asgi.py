import os

from django.core.asgi import get_asgi_application

if os.getenv("DJANGO_ENV") == "DEV":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "storyboard.settings.dev")
elif os.getenv("DJANGO_ENV") == "PROD":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "storyboard.settings.prod")