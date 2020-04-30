from rest_framework import serializers

from accounts.serializers import UserListSerializer
from items.serializers import ItemDetailSerializer, ItemListSerializer
from .models import Comment


class CommentCreateSerializer(serializers.ModelSerializer):
    user = UserListSerializer(required=False)
    item = ItemListSerializer(required=False)

    class Meta:
        model = Comment
        fields = ["id", "comment", "user", "item", "created_at"]
        read_only_fields = ["id"]


class CommentListSerializer(serializers.ModelSerializer):
    user = UserListSerializer()

    class Meta:
        model = Comment
        fields = ["id", "comment", "user", "created_at"]
        read_only_fields = ["id", "user"]


class CommentNotificationSerializer(serializers.ModelSerializer):
    item = ItemDetailSerializer()

    class Meta:
        model = Comment
        fields = ["id", "comment", "item"]
        read_only_fields = ["id", "comment", "item"]
