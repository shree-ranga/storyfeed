from django.contrib.auth import get_user_model

from rest_framework import serializers

from .models import Profile, Follow

User = get_user_model()


class ProfileAvatarSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ["avatar"]


class UserListSerializer(serializers.ModelSerializer):
    full_name = serializers.SerializerMethodField()
    profile = ProfileAvatarSerializer(required=False, many=False)

    class Meta:
        model = User
        fields = ["id", "username", "full_name", "profile"]
        read_only_fields = ["id"]

    def get_full_name(self, obj):
        return f"{obj.first_name} {obj.last_name}"


class ProfileDetailSerializer(serializers.ModelSerializer):
    total_followers = serializers.SerializerMethodField()
    total_following = serializers.SerializerMethodField()

    class Meta:
        model = Profile
        fields = ["avatar", "bio", "total_followers", "total_following"]

    def get_total_followers(self, obj):
        return obj.followers.count()

    def get_total_following(self, obj):
        return obj.following.count()


class UserDetailSerializer(serializers.ModelSerializer):
    full_name = serializers.SerializerMethodField()
    profile = ProfileDetailSerializer(required=False, many=False)

    class Meta:
        model = User
        fields = ["id", "username", "full_name", "profile"]
        read_only_fields = ["id"]

    def get_full_name(self, obj):
        return f"{obj.first_name} {obj.last_name}"


class EditProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ["avatar", "bio"]


class EditUserSerializer(serializers.ModelSerializer):
    full_name = serializers.SerializerMethodField()
    update_full_name = serializers.CharField(required=False)
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
            "update_full_name",
        ]
        read_only_fields = ["id"]
        extra_kwargs = {"username": {"required": False}}

    def to_internal_value(self, data):
        ret = super().to_internal_value(data)
        update_full_name = ret.pop("update_full_name", None)
        if update_full_name:
            split_name = update_full_name.rsplit(None, 1)
            ret["first_name"] = split_name[0]
            ret["last_name"] = split_name[1]
        return ret

    def update(self, instance, validated_data):
        instance.username = validated_data.get("username", instance.username)
        instance.first_name = validated_data.get("first_name", instance.first_name)
        instance.last_name = validated_data.get("last_name", instance.last_name)
        instance.email = validated_data.get("email", instance.email)
        instance.profile.bio = validated_data.get("bio", instance.profile.bio)
        instance.profile.avatar = validated_data.get("avatar", instance.profile.avatar)
        instance.profile.save()
        instance.save()
        return instance

    def get_full_name(self, obj):
        return f"{obj.first_name} {obj.last_name}"


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
