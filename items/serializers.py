from rest_framework import serializers

from .models import Item, Like

from accounts.serializers import UserListSerializer


class ItemCreateSerializer(serializers.ModelSerializer):
    user = UserListSerializer(required=False)

    class Meta:
        model = Item
        fields = ("id", "user", "item", "caption")
        read_only_fields = ("id", "user")


class ItemListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        fields = ("id", "item")
        read_only_fields = ("id",)


class ItemDetailSerializer(serializers.ModelSerializer):
    user = UserListSerializer()

    class Meta:
        model = Item
        fields = (
            "id",
            "user",
            "item",
            "caption",
            "created_at",
            "likes_count",
            "comments_count",
        )
        read_only_fields = ("id", "user")
