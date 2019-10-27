from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import ValidationError

from .serializers import (
    UserListSerializer,
    UserDetailSerializer,
    ProfileAvatarSerializer,
)

User = get_user_model()


class UserListAPI(APIView):
    def get(self, request, *args, **kwargs):
        queryset = User.objects.all()
        serializer = UserListSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class UserDetailAPI(APIView):
    def get_object(self, pk):
        user = get_object_or_404(User, pk=pk)
        return user

    def get(self, request, pk=None, *args, **kwargs):
        user = self.get_object(pk)
        serializer = UserDetailSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)


class UploadProfileAvatarAPI(APIView):
    def patch(self, request, *args, **kwargs):
        data = request.data
        avatar = data.get("avatar")
        profile = request.user.profile
        serializer = ProfileAvatarSerializer(
            profile, data={"avatar": avatar}, partial=True
        )
        if serializer.is_valid():
            serializer.save()
            return Response(
                {"msg": "Upload successful.."}, status=status.HTTP_201_CREATED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
