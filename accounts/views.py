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
    FollowSerializer,
)
from .models import Follow

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


class FollowUnfollowAPI(APIView):
    # follow
    def post(self, request, *args, **kwargs):
        data = request.data
        follower_user_id = request.user.id
        following_user_id = data.get("following_user_id")
        follow_data = {
            "follower_user": follower_user_id,
            "following_user": following_user_id,
        }
        serializer = FollowSerializer(data=follow_data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # unfollow
    def delete(self, request, *args, **kwargs):
        query_params = request.query_params
        follower_user_id = request.user.id
        following_user_id = query_params.get("following_user_id")
        instance = Follow.objects.get(
            follower_user_id=follower_user_id, following_user_id=following_user_id
        )
        if instance:
            instance.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(
            {"error": "Following user instance does not exist"},
            status=status.HTTP_400_BAD_REQUEST,
        )


class CheckFollowedAPI(APIView):
    def post(self, request, *args, **kwargs):
        data = request.data
        follower_user_id = request.user.id
        following_user_id = data.get("following_user_id")
        if Follow.objects.filter(
            follower_user_id=follower_user_id, following_user_id=following_user_id
        ).exists():
            return Response({"following": True}, status=status.HTTP_200_OK)
        return Response({"following": False}, status=status.HTTP_200_OK)


class UserFollowersListAPI(APIView):
    def get_object(self, pk):
        try:
            user = User.objects.get(pk=pk)
            return user
        except:
            raise ValidationError("User object does not exist")

    def get_queryset(self, pk):
        user = self.get_object(pk=pk)
        followers_ids = list(user.profile.followers.all().values_list(flat=True))
        followers = User.objects.filter(pk__in=followers_ids)
        return followers

    def get(self, request, pk=None, *args, **kwargs):
        if pk is not None:
            queryset = self.get_queryset(pk)
            serializer = UserListSerializer(queryset, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(
            {"error": "Could not fetch followers"}, status=status.HTTP_400_BAD_REQUEST
        )


class UserFollowingListAPI(APIView):
    def get_object(self, pk):
        try:
            user = User.objects.get(pk=pk)
            return user
        except:
            raise ValidationError("User object does not exist")

    def get_queryset(self, pk):
        user = self.get_object(pk=pk)
        following_ids = list(user.profile.following.all().values_list(flat=True))
        following = User.objects.filter(pk__in=following_ids)
        return following

    def get(self, request, pk=None, *args, **kwargs):
        if pk is not None:
            queryset = self.get_queryset(pk)
            serializer = UserListSerializer(queryset, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(
            {"error": "Could not fetch followers"}, status=status.HTTP_400_BAD_REQUEST
        )
