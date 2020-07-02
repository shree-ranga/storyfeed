from rest_framework import serializers

from .models import Comment

from accounts.serializers import UserListSerializer
from items.serializers import (
    ItemDetailSerializer,
    ItemListSerializer,
    ItemCommentListSerializer,
)
from notifications.models import Notification


class CommentCreateSerializer(serializers.ModelSerializer):
    user = UserListSerializer(required=False)
    item = ItemListSerializer(required=False)

    class Meta:
        model = Comment
        fields = ["id", "comment", "user", "item", "created_at"]
        read_only_fields = ["id"]

    def create(self, validated_data):
        instance = Comment.objects.create(**validated_data)

        # create notification
        if instance.user != instance.item.user:
            n_data = {
                "receiver": instance.item.user,
                "sender": instance.user,
                "content_object": instance,
                "notification_type": "comment",
            }
            n = Notification(**n_data)
            n.save()

        return instance


class CommentListSerializer(serializers.ModelSerializer):
    user = UserListSerializer()
    item = ItemCommentListSerializer()

    class Meta:
        model = Comment
        fields = ["id", "comment", "user", "created_at", "item"]
        read_only_fields = ["id", "user", "item"]


class CommentNotificationSerializer(serializers.ModelSerializer):
    item = ItemDetailSerializer()

    class Meta:
        model = Comment
        fields = ["id", "comment", "item"]
        read_only_fields = ["id", "comment", "item"]
