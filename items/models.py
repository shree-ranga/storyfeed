from django.db import models
from django.conf import settings


class Item(models.Model):
    # choices = (("portrait", "pr"), ("landscape", "ln"), ("square", "sq"))
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="item_by"
    )
    item = models.ImageField(null=True, blank=True)
    caption = models.TextField(max_length=150, null=True, blank=True)
    likes_count = models.PositiveIntegerField(default=0)
    comments_count = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ("-created_at",)

    def __str__(self):
        return f"{self.id} by {self.user.username}"


class Like(models.Model):
    item = models.ForeignKey("Item", on_delete=models.CASCADE, related_name="item_like")
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="liked_by"
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("item", "user")

    def __str__(self):
        return f"{self.user.username} liked {self.item.id}"
