from io import BytesIO

from django.contrib.auth import get_user_model
from django.core.files.storage import default_storage
from django.conf import settings

from celery import shared_task

from push_notifications.models import APNSDevice

from PIL import Image

import boto3

from notifications.models import Notification

User = get_user_model()


@shared_task
def process_avatar_image(user_id):
    try:
        memfile = BytesIO()
        user = User.objects.get(id=user_id)
        i = Image.open(user.profile.profileavatar.avatar)
        i.thumbnail(size=(300, 450))
        i.save(memfile, "JPEG")
        default_storage.save(user.profile.profileavatar.avatar.name, memfile)
        memfile.close()
        i.close()
    except Exception as e:
        print(e)


@shared_task
def send_follow_push_notification(receiver_id, sender_id):
    try:
        devices = APNSDevice.objects.filter(user=receiver_id)
    except APNSDevice.ObjectDoesNotExist:
        pass

    sender = User.objects.get(id=sender_id)

    msg = f"{sender.username} ({sender.full_name}) started following you!"
    badge_count = Notification.objects.filter(
        receiver=receiver_id, checked=False
    ).count()

    devices.send_message(message={"body": msg}, badge=badge_count)


@shared_task
def delete_reported_user(id):
    try:
        u = User.objects.get(id=id)
        u.delete()
    except:
        pass


@shared_task
def delete_profile_avatar(user_id):
    try:
        user = User.objects.get(id=user_id)
        s3_resource = boto3.resource("s3")
        s3_resource.Object(
            settings.AWS_STORAGE_BUCKET_NAME,
            f"{default_storage.location}/{user.profile.profileavatar.avatar.name}",
        ).delete()
        profile_avatar = user.profile.profileavatar
        profile_avatar.delete()
        user.save()
    except Exception as e:
        print(e)
