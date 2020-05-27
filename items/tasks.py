from django.contrib.auth import get_user_model

from celery import shared_task

from push_notifications.models import APNSDevice

import boto3

from items.models import Item

from notifications.models import Notification

User = get_user_model()


@shared_task
def delete_after_expiration(item_id):
    try:
        i = Item.objects.get(id=item_id)
        i.delete()
    except Item.ObjectDoesNotExist:
        pass


@shared_task
def send_item_like_notification(receiver_id, sender_id):
    try:
        devices = APNSDevice.objects.filter(user=receiver_id)
    except APNSDevice.ObjectDoesNotExist:
        return "No devices found"

    sender = User.objects.get(id=sender_id)

    msg = f"{sender.username} ({sender.full_name}) liked your post."
    badge_count = Notification.objects.filter(checked=False).count()

    devices.send_message(message={"body": msg}, badge=badge_count)


@shared_task
def delete_reported_item(item_id):
    try:
        i = Item.objects.get(id=item_id)
        i.delete()
    except Item.ObjectDoesNotExist:
        pass
