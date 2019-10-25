from django.contrib.auth import get_user_model

from rest_framework import serializers

from .models import Profile, Follow

User = get_user_model()


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ["bio", "avatar", "followers"]


class UserListSerializer(serializers.ModelSerializer):
    full_name = serializers.SerializerMethodField()
    profile = ProfileSerializer(required=False, many=False)

    class Meta:
        model = User
        fields = ["id", "username", "full_name", "profile"]
        read_only_fields = ["id"]

    def get_full_name(self, obj):
        return str(obj.first_name + " " + obj.last_name)

