from django.contrib.auth import get_user_model

from celery import shared_task

from push_notifications.models import APNSDevice

User = get_user_model()


@shared_task
def send_follow_push_notification(receiver_id, sender_id):
    try:
        devices = APNSDevice.objects.filter(user=receiver_id)
    except APNSDevice.DoesNotExist:
        return "APNSDevice matching query does not exist"

    sender = User.objects.get(id=sender_id)
    msg = f"{sender.username} ({sender.first_name} {sender.last_name}) started following you!"
    devices.send_message(msg)
