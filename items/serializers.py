from io import BytesIO

from django.db.models import F

from rest_framework import serializers

from .models import Item, Like

from accounts.serializers import UserListSerializer


class ItemCreateSerializer(serializers.ModelSerializer):
    user = UserListSerializer(required=False)

    class Meta:
        model = Item
        fields = ["id", "user", "item"]
        read_only_fields = ["id"]


class ItemListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        fields = ["id", "item"]
        read_only_fields = ["id"]


class ItemDetailSerializer(serializers.ModelSerializer):
    user = UserListSerializer()
    likes_count = serializers.ReadOnlyField(source="total_likes")
    comments_count = serializers.ReadOnlyField(source="total_comments")

    class Meta:
        model = Item
        fields = [
            "id",
            "user",
            "item",
            "created_at",
            "likes_count",
            "comments_count",
        ]
        read_only_fields = ["id", "user"]


class ItemCommentListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        fields = ["id"]
        read_only_fields = ["id"]


class LikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Like
        fields = ["id", "item", "user"]
        read_only_fields = ["id", "user"]


class LikeNotificationSerializer(serializers.ModelSerializer):
    item = ItemDetailSerializer()

    class Meta:
        model = Like
        fields = ["id", "item"]
        read_only_fields = ["id", "item"]
