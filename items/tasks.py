from celery import shared_task

from PIL import Image

from items.models import Item
from items.serializers import ItemCreateSerializer


@shared_task
def delete_after_expiration(item_id):
    try:
        Item.objects.get(id=item_id).delete()
    except Item.ObjectDoesNotExist:
        pass
