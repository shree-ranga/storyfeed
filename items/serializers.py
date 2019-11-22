from rest_framework import serializers

from .models import Item, Like

from accounts.serializers import UserListSerializer


class ItemSerializer(serializers.ModelSerializer):
    user = UserListSerializer(required=False)

    class Meta:
        model = Item
        fields = "__all__"
        read_only_fields = ("id", "user")
