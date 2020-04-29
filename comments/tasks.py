from django.contrib.auth import get_user_model

from celery import shared_task

from push_notifications.models import APNSDevice

from notifications.models import Notification

User = get_user_model()


@shared_task
def send_comment_notification(receiver_id, sender_id, comment):
    try:
        devices = APNSDevice.objects.filter(user=receiver_id)
    except:
        return "APNS device does not exist"

    sender = User.objects.get(id=sender_id)
    msg = f"""{sender.username} commented: "{comment}" on your post."""
    badge_count = Notification.objects.filter(checked=False).count()
    devices.send_message(message={"body": msg}, badge=badge_count)
