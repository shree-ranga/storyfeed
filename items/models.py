from django.db import models
from django.conf import settings

from django.contrib.contenttypes.fields import GenericRelation
from notifications.models import Notification


class Item(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="items"
    )
    item = models.ImageField(null=True, blank=True)
    video_url = models.CharField(max_length=300, null=True, blank=True)
    audio_url = models.CharField(max_length=300, null=True, blank=True)
    caption = models.CharField(max_length=100, null=True, blank=True)
    is_private = models.BooleanField(default=False)
    expiry_time = models.PositiveIntegerField(default=1)
    engagement_counter = models.PositiveIntegerField(default=0)
    report_counter = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ("-created_at",)

    @property
    def total_likes(self):
        return self.item_like.count()

    @property
    def single_liked_user(self):
        if self.item_like.count() > 0:
            return self.item_like.first()

    @property
    def is_more_than_one_like(self):
        if self.item_like.count() > 1:
            return True
        else:
            return False

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
    notifications = GenericRelation(Notification)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("item", "user")

    def __str__(self):
        return f"{self.user.username} liked {self.item.id}"


class HashTag(models.Model):
    items = models.ManyToManyField("Item", related_name="hashtags")
    hashtag = models.CharField(max_length=100, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.hashtag}"
