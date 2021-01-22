import json

from django.contrib.auth import get_user_model
from django.db.models import F

from rest_framework import serializers
from rest_framework.validators import ValidationError

from .models import Item, Like, HashTag

from accounts.serializers import UserListSerializer
from notifications.models import Notification

User = get_user_model()


class ItemCreateSerializer(serializers.ModelSerializer):
    user = UserListSerializer(required=False)

    class Meta:
        model = Item
        fields = [
            "id",
            "user",
            "item",
            "video_url",
            "audio_url",
            "expiry_time",
            "status_text",
            "status_red",
            "status_green",
            "status_blue",
            "caption",
            "engagement_counter",
            "is_private",
        ]
        read_only_fields = ["id"]


class ItemLikedUserSerializer(serializers.ModelSerializer):
    user = UserListSerializer()

    class Meta:
        model = Like
        fields = ["user"]
        read_only_fields = ["user"]


class HashTagSerializer(serializers.ModelSerializer):
    class Meta:
        model = HashTag
        fields = ["id", "hashtag"]
        read_only_fields = ["id"]


class ItemListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        fields = ["id", "item", "engagement_counter"]
        read_only_fields = ["id", "engagement_counter"]


class ItemDetailSerializer(serializers.ModelSerializer):
    user = UserListSerializer()
    single_liked_user = ItemLikedUserSerializer()
    hashtags = HashTagSerializer(many=True)
    comments_count = serializers.ReadOnlyField(source="total_comments")
    likes_count = serializers.ReadOnlyField(source="total_likes")

    class Meta:
        model = Item
        fields = [
            "id",
            "user",
            "item",
            "video_url",
            "audio_url",
            "status_text",
            "status_red",
            "status_green",
            "status_blue",
            "caption",
            "hashtags",
            "created_at",
            "engagement_counter",
            "single_liked_user",
            "is_more_than_one_like",
            "comments_count",
            "likes_count",
        ]
        read_only_fields = [
            "id",
            "user",
            "engagement_counter",
            "single_liked_user",
            "is_more_than_one_like",
            "hashtags",
        ]


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

        # update likes count of the user
        user = User.objects.get(id=instance.item.user.id)
        user.profile.total_likes = F("total_likes") + 1
        user.profile.save()
        user.save()

        # create notification object
        if instance.user != instance.item.user:
            n_data = {
                "receiver": instance.item.user,
                "sender": instance.user,
                "content_object": instance,
                "notification_type": "like",
            }
            n = Notification(**n_data)
            n.save()

        return instance


class LikeNotificationSerializer(serializers.ModelSerializer):
    item = ItemDetailSerializer()

    class Meta:
        model = Like
        fields = ["id", "item"]
        read_only_fields = ["id", "item"]
