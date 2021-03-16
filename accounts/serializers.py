from django.contrib.auth import get_user_model

from rest_framework import serializers

from .models import Profile, Follow, ProfileAvatar

from notifications.models import Notification

User = get_user_model()


class ProfileAvatarSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProfileAvatar
        fields = ["avatar"]


class ProfilePicSerializer(serializers.ModelSerializer):
    profileavatar = ProfileAvatarSerializer(required=False, many=False)

    class Meta:
        model = Profile
        fields = ["profileavatar"]


class UserListSerializer(serializers.ModelSerializer):
    profile = ProfilePicSerializer(required=False, many=False)

    class Meta:
        model = User
        fields = ["id", "username", "full_name", "profile"]
        read_only_fields = ["id"]


class ProfileDetailSerializer(serializers.ModelSerializer):
    total_followers = serializers.ReadOnlyField(source="followers_count")
    total_following = serializers.ReadOnlyField(source="following_count")
    total_likes = serializers.ReadOnlyField(source="item_likes")
    profileavatar = ProfileAvatarSerializer(required=False, many=False)

    class Meta:
        model = Profile
        fields = [
            "bio",
            "total_followers",
            "total_following",
            "total_likes",
            "profileavatar",
        ]


class UserDetailSerializer(serializers.ModelSerializer):
    profile = ProfileDetailSerializer(required=False, many=False)

    class Meta:
        model = User
        fields = ["id", "username", "full_name", "profile"]
        read_only_fields = ["id"]


class ProfileBioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ["bio"]


# TODO: - think and refactor
class EditUserSerializer(serializers.ModelSerializer):
    bio = serializers.CharField(required=False)
    profile = ProfileBioSerializer(required=False)

    class Meta:
        model = User
        fields = [
            "id",
            "username",
            "full_name",
            "bio",
            "profile",
            "email",
        ]
        read_only_fields = ["id"]
        extra_kwargs = {"username": {"required": False}}

    def update(self, instance, validated_data):
        instance.username = validated_data.get("username", instance.username)
        instance.full_name = validated_data.get("full_name", instance.full_name)
        instance.email = validated_data.get("email", instance.email)
        instance.profile.bio = validated_data.get("bio", None)
        instance.save()
        instance.profile.save()
        return instance


class UserNotificationSerializer(serializers.ModelSerializer):
    profile = ProfilePicSerializer()

    class Meta:
        model = User
        fields = ["id", "username", "profile"]
        read_only_fields = ["id", "username", "profile"]


class FollowSerializer(serializers.ModelSerializer):
    class Meta:
        model = Follow
        fields = ["id", "following_user", "follower_user"]
        read_only_fields = ["id"]

    def create(self, validated_data):
        instance = Follow.objects.create(**validated_data)

        # create notification
        n_data = {
            "receiver": instance.following_user.user,
            "sender": instance.follower_user.user,
            "content_object": instance,
            "notification_type": "follow",
        }
        n = Notification(**n_data)
        n.save()

        return instance


class FollowNotificationSerialzier(serializers.ModelSerializer):
    class Meta:
        model = Follow
        fields = ["id", "following_user"]
        read_only_fields = ["id", "following_user"]


# class BlockUserSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Profile
#         fields = ["id", "blocked_profiles"]
