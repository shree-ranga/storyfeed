import os

from django.core.wsgi import get_wsgi_application

if os.getenv("DJANGO_ENV") == "DEV":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "storyboard.settings.dev")
elif os.getenv("DJANGO_ENV") == "PROD":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "storyboard.settings.prod")

application = get_wsgi_application()
