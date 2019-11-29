from rest_framework import serializers

from accounts.serializers import UserListSerializer

from .models import Comment


class CommentCreateSerializer(serializers.ModelSerializer):
    user = UserListSerializer(required=False)

    class Meta:
        model = Comment
        fields = ["id", "comment", "user", "item"]
        read_only_fields = ["id"]

class CommentListSerializer(serializers.ModelSerializer):
    user = UserListSerializer()
    class Meta:
        model = Comment
        fields = ["id", "comment", "user"]
        read_only_fields = ["id", "user"]