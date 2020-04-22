from django.contrib.auth import get_user_model

from celery import shared_task

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
def send_item_like_notification():
    pass
