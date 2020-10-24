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
    hashTags = serializers.CharField()

    class Meta:
        model = Item
        fields = [
            "id",
            "user",
            "item",
            "video_url",
            "audio_url",
            "expiry_time",
            "caption",
            "engagement_counter",
            "is_private",
            "hashTags",
        ]
        read_only_fields = ["id"]

    def create(self, validated_data):
        h = json.loads(validated_data.pop("hashTags"))
        instance = Item.objects.create(**validated_data)

        if h is not None:
            words = h["hashTags"]
            for word in words:
                tag_instance, created = HashTag.objects.get_or_create(hashtag=word)
                tag_instance.items.add(instance)
                tag_instance.save()

        return instance


class ItemListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        fields = ["id", "item", "engagement_counter"]
        read_only_fields = ["id", "engagement_counter"]


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
            "video_url",
            "audio_url",
            "caption",
            "likes_count",
            "comments_count",
            "created_at",
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


class HashTagSerializer(serializers.ModelSerializer):
    class Meta:
        model = HashTag
        fields = "__all__"
        read_only_fields = ["id"]