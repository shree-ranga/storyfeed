from celery import shared_task

from items.models import Item


@shared_task
def delete_after_expiration(item_id):
    try:
        Item.objects.get(id=item_id).delete()
    except Item.ObjectDoesNotExist:
        pass
