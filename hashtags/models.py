from django.db import models

from items.models import Item


class Hashtag(models.Model):
    item = models.ManyToManyField(Item, symmetrical=False, related_name="items")
    text = models.CharField(max_length=150, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"hashtag text for item {self.item.id} is {self.text}"
