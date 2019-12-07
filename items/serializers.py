from django.db.models import F

from rest_framework import serializers

from .models import Item, Like

from accounts.serializers import UserListSerializer


class ItemCreateSerializer(serializers.ModelSerializer):
    user = UserListSerializer(required=False)

    class Meta:
        model = Item
        fields = ["id", "user", "item", "caption"]
        read_only_fields = ["id"]


class ItemListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        fields = ["id", "item"]
        read_only_fields = ["id"]


class ItemDetailSerializer(serializers.ModelSerializer):
    user = UserListSerializer()
    likes_count = serializers.SerializerMethodField()
    comments_count = serializers.SerializerMethodField()

    def get_likes_count(self, obj):
        return obj.item_like.count()

    def get_comments_count(self, obj):
        return obj.item_comments.count()

    class Meta:
        model = Item
        fields = [
            "id",
            "user",
            "item",
            "caption",
            "created_at",
            "likes_count",
            "comments_count",
        ]
        read_only_fields = ["id", "user"]


class LikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Like
        fields = ["id", "item", "user"]
        read_only_fields = ["id", "user"]


class LikeNotificationSerializer(serializers.ModelSerializer):
    item = ItemListSerializer()

    class Meta:
        model = Like
        fields = ["id", "item"]
        read_only_fields = ["id", "item"]
