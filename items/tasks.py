from django.contrib.auth import get_user_model
from django.conf import settings

from celery import shared_task

from push_notifications.models import APNSDevice

import boto3

# import redis

from items.models import Item

from notifications.models import Notification

from storyboard.storage_backends import MediaStorage

User = get_user_model()
# r = redis.StrictRedis(db=1, decode_responses=True)


@shared_task
def send_item_like_notification(receiver_id, sender_id):
    try:
        devices = APNSDevice.objects.filter(user=receiver_id)
    except APNSDevice.ObjectDoesNotExist:
        pass

    sender = User.objects.get(id=sender_id)

    msg = f"{sender.username} ({sender.full_name}) liked your story!"
    badge_count = Notification.objects.filter(checked=False).count()

    devices.send_message(message={"body": msg}, badge=badge_count)


# @shared_task
# def push_model(user: User, post_id):
#     max_length = 10
#     follower_ids = user.profile.followers.all().values_list(flat=True)
#     with r.pipeline() as pipe:
#         for ids in follower_ids:
#             pipe.lpush(f"homefeed:{user.id}", post_id)
#             pipe.ltrim(f"homefeed:{user.id}", 0, max_length - 1)
#         pipe.execute()


# @shared_task
# def send_official_notification():
#     devices = APNSDevice.objects.all()
#     msg = f"Check out new story from official @storyfeed account."
#     devices.send_message(msg)


# @shared_task
# def delete_reported_item(item_id):
#     try:
#         i = Item.objects.get(id=item_id)
#         i.delete()
#     except Item.ObjectDoesNotExist:
#         pass


@shared_task
def delete_item(item_id):
    try:
        i = Item.objects.get(id=item_id)
        s3_resource = boto3.resource("s3")
        s3_resource.Object(
            settings.AWS_STORAGE_BUCKET_NAME, f"{MediaStorage.location}/{i.item.name}"
        ).delete()
        i.delete()
    except:
        pass
