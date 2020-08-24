from django.db import models
from django.conf import settings

from django.contrib.contenttypes.fields import GenericRelation

from notifications.models import Notification


class Item(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="item_by"
    )
    item = models.ImageField(null=True, blank=True)
    video_url = models.CharField(max_length=300, null=True, blank=True)
    caption = models.CharField(max_length=100, null=True, blank=True)
    expiry_time = models.PositiveIntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    report_counter = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ("-created_at",)

    @property
    def total_likes(self):
        return self.item_like.count()

    @property
    def total_comments(self):
        return self.item_comments.count()

    def __str__(self):
        return f"{self.id} by {self.user.username}"


class Like(models.Model):
    item = models.ForeignKey("Item", on_delete=models.CASCADE, related_name="item_like")
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="liked_by"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    notifications = GenericRelation(Notification)

    class Meta:
        unique_together = ("item", "user")

    def __str__(self):
        return f"{self.user.username} liked {self.item.id}"
