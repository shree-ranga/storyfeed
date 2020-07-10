from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from django.core.files.storage import default_storage
from django.db.models import F, Q

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
from .models import Follow, ProfileAvatar
from .pagination import UserSearchPagination, UserFollowerFollowingPagination
from .permissions import IsOwnerOrAdmin
from .tasks import (
    send_follow_push_notification,
    process_avatar_image,
    delete_profile_avatar,
)

User = get_user_model()


class ProfileAvatarAPI(APIView):
    def post(self, request, *args, **kwargs):
        avatar = request.data.get("avatar")
        data = {"avatar": avatar}
        serializer = ProfileAvatarSerializer(data=data)
        if serializer.is_valid():
            serializer.save(profile=request.user.profile)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, *args, **kwargs):
        avatar = request.data.get("avatar")
        profile = self.request.user.profile
        avatar_instance = ProfileAvatar(profile=profile)
        data = {"avatar": avatar}
        serializer = ProfileAvatarSerializer(avatar_instance, data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, *args, **kwargs):
        profile_avatar = request.user.profile.profileavatar
        delete_profile_avatar.delay(request.user.id)
        return Response(status=status.HTTP_204_NO_CONTENT)


class UserListAPI(generics.ListAPIView):
    filter_backends = [SearchFilter]
    search_fields = ["username", "full_name"]
    pagination_class = UserSearchPagination

    # TODO: - refactor blocking logic
    def get_queryset(self):
        blocked_by_ids = list(self.request.user.blocked_by.all().values_list(flat=True))
        blocked_profile_ids = list(
            self.request.user.profile.blocked_profiles.all().values_list(flat=True)
        )
        block_list_ids = blocked_by_ids + blocked_profile_ids
        users = User.objects.exclude(pk__in=block_list_ids)
        return users

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
    def post(self, request, *args, **kwargs):
        following_user_id = request.data.get("following_user_id")
        follow_data = {
            "follower_user": request.user.id,
            "following_user": following_user_id,
        }
        serializer = FollowSerializer(data=follow_data)
        if serializer.is_valid():
            serializer.save()

            send_follow_push_notification.delay(
                receiver_id=serializer.instance.following_user_id,
                sender_id=serializer.instance.follower_user_id,
            )

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

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


class ReportUserAPI(APIView):
    def post(self, request, *args, **kwargs):
        reporting_id = request.data.get("reporting_id")
        user = User.objects.get(id=reporting_id)
        user.profile.report_count = F("report_count") + 1
        user.profile.save()
        return Response(status=status.HTTP_201_CREATED)


class BlockUnblockUserAPI(APIView):
    def get(self, request, *args, **kwargs):
        blocked_users = self.request.user.profile.blocked_profiles.all()
        serializer = UserListSerializer(blocked_users, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        blocking_id = request.data.get("blocking_id")
        request.user.profile.blocked_profiles.add(blocking_id)
        request.user.profile.save()
        follower_user_id = request.user.id

        try:
            following_instance = Follow.objects.get(
                follower_user_id=follower_user_id, following_user_id=blocking_id
            )
            following_instance.delete()
        except Exception as e:
            pass

        try:
            follower_instance = Follow.objects.get(
                follower_user_id=blocking_id, following_user_id=follower_user_id
            )
            follower_instance.delete()
        except Exception as e:
            pass

        return Response(status=status.HTTP_201_CREATED)

    def delete(self, request, *args, **kwargs):
        unblocking_id = request.query_params.get("unblocking_id")
        request.user.profile.blocked_profiles.remove(unblocking_id)
        request.user.profile.save()
        return Response(status=status.HTTP_204_NO_CONTENT)
