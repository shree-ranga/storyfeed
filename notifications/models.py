from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from django.conf import settings


class Notification(models.Model):
    NOTIFICATION_TYPE = (("like", "Like"), ("follow", "Follow"), ("comment", "Comment"))
    receiver = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name="notification_to",
        on_delete=models.CASCADE,
    )
    sender = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name="notification_from",
        on_delete=models.CASCADE,
    )
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey("content_type", "object_id")
    notification_type = models.CharField(max_length=20, choices=NOTIFICATION_TYPE)
    checked = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ("-created_at",)

    def __str__(self):
        return f"notification_id-{self.id} {self.sender} -> {self.notification_type} -> {self.receiver}"
