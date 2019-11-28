from rest_framework import serializers

from accounts.serializers import UserListSerializer

from .models import Comment


class CommentSerializer(serializers.ModelSerializer):
    user = UserListSerializer(required=False)

    class Meta:
        model = Comment
        fields = ["id", "comment", "user", "item"]
        read_only_fields = ["id"]

