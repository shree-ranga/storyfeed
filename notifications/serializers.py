from django.contrib.contenttypes.models import ContentType

from rest_framework import serializers

from .models import Notification

from accounts.models import Follow
from accounts.serializers import (
    FollowNotificationSerialzier,
    UserNotificationSerializer,
)

from items.models import Like
from items.serializers import LikeNotificationSerializer

from comments.models import Comment
from comments.serializers import CommentNotificationSerializer


class NotifiedObjectRelatedField(serializers.RelatedField):
    def to_internal_value(self, value):
        if isinstance(value, Follow):
            return value
        elif isinstance(value, Like):
            return value
        elif isinstance(value, Comment):
            return value
        else:
            raise Exception("Unexpected content object")

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


class NotificationListSerializer(serializers.ModelSerializer):
    content_object = NotifiedObjectRelatedField(read_only=True)
    sender = UserNotificationSerializer(required=False)

    class Meta:
        model = Notification
        fields = ["id", "sender", "content_object", "notification_type", "created_at"]
        read_only_fields = ["id", "sender"]

    def to_representation(self, instance):
        return super().to_representation(instance)


class NotificationSerializer(serializers.ModelSerializer):
    content_object = NotifiedObjectRelatedField(queryset=ContentType.objects.all())

    class Meta:
        model = Notification
        fields = ["sender", "receiver", "content_object", "notification_type"]
