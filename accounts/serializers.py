from django.contrib.auth import get_user_model

from rest_framework import serializers

from .models import Profile, Follow

User = get_user_model()


class ProfileAvatarSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ["avatar"]


class UserListSerializer(serializers.ModelSerializer):
    profile = ProfileAvatarSerializer(required=False, many=False)

    class Meta:
        model = User
        fields = ["id", "username", "full_name", "profile"]
        read_only_fields = ["id"]


class ProfileDetailSerializer(serializers.ModelSerializer):
    total_followers = serializers.ReadOnlyField(source="followers_count")
    total_following = serializers.ReadOnlyField(source="following_count")

    class Meta:
        model = Profile
        fields = ["avatar", "bio", "total_followers", "total_following"]


class UserDetailSerializer(serializers.ModelSerializer):
    profile = ProfileDetailSerializer(required=False, many=False)

    class Meta:
        model = User
        fields = ["id", "username", "full_name", "profile"]
        read_only_fields = ["id"]


class EditProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ["avatar", "bio"]


class EditUserSerializer(serializers.ModelSerializer):
    bio = serializers.CharField(required=False)
    profile = EditProfileSerializer(read_only=True)
    avatar = serializers.ImageField(required=False)

    class Meta:
        model = User
        fields = [
            "id",
            "username",
            "full_name",
            "bio",
            "profile",
            "avatar",
            "email",
        ]
        read_only_fields = ["id"]
        extra_kwargs = {"username": {"required": False}}

    def update(self, instance, validated_data):
        instance.username = validated_data.get("username", instance.username)
        instance.full_name = validated_data.get("full_name", instance.full_name)
        instance.email = validated_data.get("email", instance.email)
        instance.profile.bio = validated_data.get("bio", instance.profile.bio)
        instance.profile.avatar = validated_data.get("avatar", instance.profile.avatar)
        instance.save()
        instance.profile.save()
        return instance


class UserNotificationSerializer(serializers.ModelSerializer):
    profile = ProfileAvatarSerializer()

    class Meta:
        model = User
        fields = ["id", "username", "profile"]
        read_only_fields = ["id", "username", "profile"]


class FollowSerializer(serializers.ModelSerializer):
    class Meta:
        model = Follow
        fields = ["id", "following_user", "follower_user"]
        read_only_fields = ["id"]


class FollowNotificationSerialzier(serializers.ModelSerializer):
    class Meta:
        model = Follow
        fields = ["id", "following_user"]
        read_only_fields = ["id", "following_user"]
