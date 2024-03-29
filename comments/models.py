from django.db import models
from django.conf import settings

from items.models import Item

from django.contrib.contenttypes.fields import GenericRelation

from notifications.models import Notification


class Comment(models.Model):
    comment = models.CharField(max_length=2200, null=True, blank=True)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="comment_by"
    )
    item = models.ForeignKey(
        Item, on_delete=models.CASCADE, related_name="item_comments"
    )
    report_count = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    notifications = GenericRelation(Notification)

    class Meta:
        ordering = ("created_at",)

    def __str__(self):
        return f"{self.comment} by {self.user.username} on post {self.item.id}"


class CommentLike(models.Model):
    pass
