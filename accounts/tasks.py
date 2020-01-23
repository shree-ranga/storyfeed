from django.contrib.auth import get_user_model

from celery import shared_task

from push_notifications.models import APNSDevice

User = get_user_model()


@shared_task
def send_follow_push_notification(receiver_id, sender_id, device_id):
    try:
        device = APNSDevice.objects.get(user=receiver_id, device_id=device_id)
    except:
        APNSDevice.ObjectDoesNotExist

    try:
        receiver = User.objects.get(id=receiver_id)
    except:
        User.ObjectDoesNotExist

    try:
        sender = User.objects.get(id=sender_id)
    except:
        User.ObjectDoesNotExist

    msg = f"{sender.username} stared following you!"

    device.send_message(msg)
