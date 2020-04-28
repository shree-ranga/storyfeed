from django.contrib.auth import get_user_model

from celery import shared_task

from push_notifications.models import APNSDevice

from items.models import Item
from items.serializers import ItemCreateSerializer

User = get_user_model()


@shared_task
def delete_after_expiration(item_id):
    try:
        Item.objects.get(id=item_id).delete()
    except Item.ObjectDoesNotExist:
        pass


@shared_task
def send_item_like_notification(receiver_id, sender_id):
    try:
        devices = APNSDevice.objects.filter(user=receiver_id)
    except:
        return "APNS device does not exist"

    sender = User.objects.get(id=sender_id)
    msg = f"{sender.username} ({sender.first_name} {sender.last_name}) liked your post."
    devices.send_message(msg)
