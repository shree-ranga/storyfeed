from django.db import models
from django.conf import settings
from django.core.validators import URLValidator
from django.contrib.contenttypes.fields import GenericRelation


from notifications.models import Notification


class Item(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="item_by"
    )
    item = models.ImageField(null=True, blank=True)
    report_counter = models.IntegerField(default=0)
    notifications = GenericRelation(Notification)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ("-created_at",)

    def save(self, *args, **kwargs):
        return super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.id} by {self.user.username}"


class Like(models.Model):
    item = models.ForeignKey("Item", on_delete=models.CASCADE, related_name="item_like")
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="liked_by"
    )
    notifications = GenericRelation(Notification)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("item", "user")

    def __str__(self):
        return f"{self.user.username} liked {self.item.id}"
