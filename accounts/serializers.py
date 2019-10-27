from django.contrib.auth import get_user_model

from rest_framework import serializers

from .models import Profile, Follow

User = get_user_model()


class ProfileAvatarSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ["avatar"]


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


class UserListSerializer(serializers.ModelSerializer):
    full_name = serializers.SerializerMethodField()
    profile = ProfileAvatarSerializer(required=False, many=False)

    class Meta:
        model = User
        fields = ["id", "username", "full_name", "profile"]
        read_only_fields = ["id"]

    def get_full_name(self, obj):
        return str(obj.first_name + " " + obj.last_name)


class UserDetailSerializer(serializers.ModelSerializer):
    full_name = serializers.SerializerMethodField()
    profile = ProfileDetailSerializer(required=False, many=False)

    class Meta:
        model = User
        fields = ["id", "username", "full_name", "profile"]
        read_only_fields = ["id"]

    def get_full_name(self, obj):
        return str(obj.first_name + " " + obj.last_name)
