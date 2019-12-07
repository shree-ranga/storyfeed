from rest_framework import serializers

from .models import Notification
from accounts.models import Follow
from items.models import Like
from comments.models import Comment
from comments.serializers import CommentNotificationSerializer
from accounts.serializers import (
    FollowNotificationSerialzier,
    UserNotificationSerializer,
)
from items.serializers import LikeNotificationSerializer


class NotifiedObjectRelatedField(serializers.RelatedField):
    def to_representation(self, value):
        if isinstance(value, Follow):
            serializer = FollowNotificationSerialzier(value)
        elif isinstance(value, Like):
            serializer = LikeNotificationSerializer(value)
        elif isinstance(value, Comment):
            serializer = CommentNotificationSerializer(value)
        else:
            raise Exception("Unexpected content object")
        return serializer.data


class NotificationSerializer(serializers.ModelSerializer):
    content_object = NotifiedObjectRelatedField(read_only=True)
    sender = UserNotificationSerializer(required=False)

    class Meta:
        model = Notification
        fields = ["id", "sender", "content_object", "notification_type", "created_at"]
        read_only_fields = ["id", "sender"]
