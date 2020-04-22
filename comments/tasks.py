from django.contrib.auth import get_user_model

from celery import shared_task

User = get_user_model()


@shared_task
def send_comment_notification():
    pass
