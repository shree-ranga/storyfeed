from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import AllowAny
from rest_framework.authtoken.models import Token

from .serializers import (
    LoginSerializer,
    LogoutSerializer,
    RegisterSerializer,
    PasswordChangeSerializer,
)
from accounts.models import Profile, ProfileAvatar

User = get_user_model()


# needs caching
class CheckUserExistsAPI(APIView):
    permission_classes = [AllowAny]

    def get(self, request, *args, **kwargs):
        username = request.query_params["username"]
        check_user_exists = User.objects.filter(username=username).exists()
        if check_user_exists:
            return Response({"exists": True}, status=status.HTTP_200_OK)
        else:
            return Response({"exists": False}, status=status.HTTP_200_OK)


class CheckEmailExistsAPI(APIView):
    permission_classes = [AllowAny]

    def get(self, request, *args, **kwargs):
        email = request.query_params["email"]
        check_email_exists = User.objects.filter(email=email).exists()
        if check_email_exists:
            return Response({"exists": True}, status=status.HTTP_200_OK)
        else:
            return Response({"exists": False}, status=status.HTTP_200_OK)


class RegisterAPI(APIView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        data = request.data
        serializer = RegisterSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            # create profile for new user
            Profile.objects.create(user=serializer.instance)
            # generate token for new user
            token = Token.objects.create(user=serializer.instance)
            return Response(
                {
                    "token": token.key,
                    "id": token.user.id,
                    "username": token.user.username,
                    "fullname": token.user.full_name,
                    "email": token.user.email,
                },
                status=status.HTTP_201_CREATED,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginAPI(APIView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        data = request.data
        serializer = LoginSerializer(data=data)
        if serializer.is_valid():
            user = serializer.validated_data.get("user")
            token, created = Token.objects.get_or_create(user=user)
            if ProfileAvatar.objects.filter(profile=user.profile).exists():
                useravatar = token.user.profile.profileavatar.avatar_url
            else:
                useravatar = None
            return Response(
                {
                    "token": token.key,
                    "id": token.user.id,
                    "username": token.user.username,
                    "fullname": token.user.full_name,
                    "email": token.user.email,
                    "avatar": useravatar,
                    "bio": token.user.profile.bio,
                },
                status=status.HTTP_200_OK,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LogoutAPI(APIView):
    pass
    # def delete(self, request, *args, **kwargs):
    #     pass
    #     # token = Token.objects.get(user=request.user)
    #     # token.delete()
    #     # return Response(status=status.HTTP_204_NO_CONTENT)


class ChangePasswordAPI(APIView):
    def put(self, request, *args, **kwargs):
        user = request.user
        password = request.data.get("password")
        data = {"password": password}
        serializer = PasswordChangeSerializer(user, data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class DeleteUserAPI(APIView):
    def delete(self, request, *args, **kwargs):
        instance = request.user
        instance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
