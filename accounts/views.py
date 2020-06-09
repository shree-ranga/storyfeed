from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.filters import SearchFilter
from rest_framework import generics

from .serializers import (
    UserListSerializer,
    UserDetailSerializer,
    ProfileAvatarSerializer,
    FollowSerializer,
    EditUserSerializer,
)
from .models import Follow
from .pagination import UserSearchPagination, UserFollowerFollowingPagination
from .permissions import IsOwnerOrAdmin
from .tasks import send_follow_push_notification

from notifications.serializers import NotificationSerializer

User = get_user_model()


class UserListAPI(generics.ListAPIView):
    filter_backends = [SearchFilter]
    search_fields = ["username", "full_name"]
    pagination_class = UserSearchPagination

    def get_queryset(self):
        return User.objects.all()

    def get_serializer(self, *args, **kwargs):
        serializer_class = self.get_serializer_class()
        return serializer_class(*args, **kwargs)

    def get_serializer_class(self):
        return UserListSerializer


class UserDetailAPI(APIView):
    def get_object(self, pk):
        user = get_object_or_404(User, pk=pk)
        return user

    def get(self, request, pk=None, *args, **kwargs):
        user = self.get_object(pk)
        serializer = UserDetailSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)


class ProfileAvatarAPI(APIView):
    def patch(self, request, *args, **kwargs):
        data = request.data
        print(data)
        avatar = data.get("avatar")
        profile = request.user.profile
        serializer = ProfileAvatarSerializer(
            profile, data={"avatar": avatar}, partial=True
        )
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, *args, **kwargs):
        profile_avatar = request.user.profile.avatar
        profile_avatar.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class EditUserView(APIView):
    permission_classes = [IsOwnerOrAdmin]

    def put(self, request, *args, **kwargs):
        data = request.data
        serializer = EditUserSerializer(request.user, data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserFollowUnfollowAPI(APIView):
    # follow
    def post(self, request, *args, **kwargs):
        following_user_id = request.data.get("following_user_id")
        follow_data = {
            "follower_user": request.user.id,
            "following_user": following_user_id,
        }
        serializer = FollowSerializer(data=follow_data)
        if serializer.is_valid():
            serializer.save()

            notification_data = {
                "receiver": serializer.instance.following_user_id,
                "sender": serializer.instance.follower_user_id,
                "content_object": serializer.instance,
                "notification_type": "follow",
            }
            notification_serializer = NotificationSerializer(data=notification_data)
            if notification_serializer.is_valid():
                notification_serializer.save()
                send_follow_push_notification.delay(
                    receiver_id=notification_serializer.instance.receiver_id,
                    sender_id=notification_serializer.instance.sender_id,
                )
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
    def get(self, request, *args, **kwargs):
        data = request.query_params
        follower_user_id = request.user.id
        following_user_id = data.get("following_user_id")
        if Follow.objects.filter(
            follower_user_id=follower_user_id, following_user_id=following_user_id
        ).exists():
            return Response({"following": True}, status=status.HTTP_200_OK)
        return Response({"following": False}, status=status.HTTP_200_OK)


class UserFollowersListAPI(generics.ListAPIView):
    pagination_class = UserFollowerFollowingPagination

    def get_object(self):
        pk = self.kwargs["pk"]
        try:
            user = User.objects.get(pk=pk)
            return user
        except:
            raise ValidationError("User object does not exist")

    def get_queryset(self):
        user = self.get_object()
        followers_ids = list(user.profile.followers.all().values_list(flat=True))
        followers = User.objects.filter(pk__in=followers_ids)
        return followers

    def get_serializer(self, *args, **kwargs):
        serializer_class = self.get_serializer_class()
        return serializer_class(*args, **kwargs)

    def get_serializer_class(self):
        return UserListSerializer


class UserFollowingListAPI(generics.ListAPIView):
    pagination_class = UserFollowerFollowingPagination

    def get_object(self):
        pk = self.kwargs["pk"]
        try:
            user = User.objects.get(pk=pk)
            return user
        except:
            raise ValidationError("User object does not exist")

    def get_queryset(self):
        user = self.get_object()
        following_ids = list(user.profile.following.all().values_list(flat=True))
        following = User.objects.filter(pk__in=following_ids)
        return following

    def get_serializer(self, *args, **kwargs):
        serializer_class = self.get_serializer_class()
        return serializer_class(*args, **kwargs)

    def get_serializer_class(self):
        return UserListSerializer
