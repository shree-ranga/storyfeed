from django.contrib.auth import get_user_model
from django.db.models import F

from rest_framework import serializers
from rest_framework.validators import ValidationError

from .models import Item, Like

from accounts.serializers import UserListSerializer

User = get_user_model()


class ItemCreateSerializer(serializers.ModelSerializer):
    user = UserListSerializer(required=False)

    class Meta:
        model = Item
        fields = ["id", "user", "item", "expiry_time"]
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
        read_only_fields = ["id"]

    def create(self, validated_data):
        instance = Like.objects.create(**validated_data)

        # update likes count for the user
        user = User.objects.get(id=instance.item.user.id)
        user.profile.total_likes = F("total_likes") + 1
        user.profile.save()
        user.save()

        return instance


class LikeNotificationSerializer(serializers.ModelSerializer):
    item = ItemDetailSerializer()

    class Meta:
        model = Like
        fields = ["id", "item"]
        read_only_fields = ["id", "item"]
