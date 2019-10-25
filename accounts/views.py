from django.contrib.auth import get_user_model

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import ValidationError

from .serializers import UserListSerializer, ProfileSerializer

User = get_user_model()


class UserListAPI(APIView):
    def get(self, request, *args, **kwargs):
        queryset = User.objects.all()
        serializer = UserListSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class UploadProfileAvatarAPI(APIView):
    def patch(self, request, *args, **kwargs):
        data = request.data
        avatar = data.get("avatar")
        profile = request.user.profile
        serializer = ProfileSerializer(profile, data={"avatar": avatar}, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
