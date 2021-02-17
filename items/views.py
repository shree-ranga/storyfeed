import datetime

from django.db.models import F, Q
from django.contrib.auth import get_user_model
from django.conf import settings
from django.core.files.storage import default_storage

from rest_framework.views import APIView
from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status

import boto3
from botocore.client import Config

from .models import Item, Like, HashTag
from .serializers import (
    ItemCreateSerializer,
    ItemListSerializer,
    ItemDetailSerializer,
    FeedItemUserListSerializer,
    LikeSerializer,
    ItemLikedUserSerializer,
)
from .pagination import (
    UserItemListPagination,
    ExploreItemListPagination,
    HashTagItemListPagination,
    FeedPagination,
    PostLikedUserPagination,
)
from .permissions import IsOwnerOrAdmin
from .tasks import delete_item, send_item_like_notification, create_hashtags

from notifications.serializers import NotificationSerializer

User = get_user_model()


class ItemCreateView(APIView):
    def post(self, request, *args, **kwargs):
        item = request.data.get("item")
        video_url = request.data.get("video_url")
        audio_url = request.data.get("audio_url")
        status_text = request.data.get("status_text")
        status_red = request.data.get("status_red")
        status_green = request.data.get("status_green")
        status_blue = request.data.get("status_blue")
        caption = request.data.get("caption")
        hashTags = request.data.get("hashTags")
        data = {
            "item": item,
            "video_url": video_url,
            "audio_url": audio_url,
            "caption": caption,
            "status_text": status_text,
            "status_red": status_red,
            "status_green": status_green,
            "status_blue": status_blue,
        }

        serializer = ItemCreateSerializer(data=data)
        if serializer.is_valid():
            serializer.save(user=request.user)

            # celery tasks
            delete_eta = serializer.instance.created_at + datetime.timedelta(days=7)
            delete_item.apply_async(args=(serializer.instance.id,), eta=delete_eta)

            if hashTags is not None:
                create_hashtags.apply_async((serializer.instance.id, hashTags))

            return Response(status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UpdateEngagementCounterView(APIView):
    def patch(self, *args, **kwargs):
        post_id = self.request.data.get("postId")
        instance = Item.objects.get(id=post_id)
        instance.engagement_counter = F("engagement_counter") + 1
        instance.save()
        return Response(status=status.HTTP_201_CREATED)


class FeedItemsListView(generics.ListAPIView):
    pagination_class = FeedPagination

    def get_queryset(self):
        user = self.request.user
        following_ids = list(user.profile.following.all().values_list(flat=True))
        following_ids.append(user.id)
        q = (
            Item.objects.filter(user__in=following_ids)
            .order_by("user", "-created_at")
            .distinct("user")
            .values_list("id", flat=True)
        )
        queryset = Item.objects.filter(id__in=q)
        return queryset

    def get_serializer(self, *args, **kwargs):
        serializer_class = self.get_serializer_class()
        return serializer_class(*args, **kwargs)

    def get_serializer_class(self):
        return FeedItemUserListSerializer


class ProfileItemListView(generics.ListAPIView):
    pagination_class = UserItemListPagination

    def get_queryset(self):
        user_id = self.request.query_params.get("uid", None)
        if user_id:
            filtered_items = Item.objects.filter(user=user_id)
        return filtered_items

    def get_serializer(self, *args, **kwargs):
        serializer_class = self.get_serializer_class()
        return serializer_class(*args, **kwargs)

    def get_serializer_class(self):
        return ItemDetailSerializer


class ExploreItemsListView(generics.ListAPIView):
    pagination_class = ExploreItemListPagination

    def get_queryset(self):
        user = self.request.user
        blocked_by_ids = list(user.blocked_by.all().values_list(flat=True))
        blocked_profile_ids = list(
            user.profile.blocked_profiles.all().values_list(flat=True)
        )
        block_list_ids = blocked_by_ids + blocked_profile_ids
        following_ids = list(user.profile.following.all().values_list(flat=True))
        following_ids.append(user.id)
        queryset = Item.objects.exclude(
            Q(user__in=following_ids) | Q(user__in=block_list_ids)
        )
        return queryset

    def get_serializer(self, *args, **kwargs):
        serializer_class = self.get_serializer_class()
        return serializer_class(*args, **kwargs)

    def get_serializer_class(self):
        return ItemDetailSerializer


class HashTagItemListView(generics.ListAPIView):
    pagination_class = HashTagItemListPagination

    def get_queryset(self):
        user = self.request.user
        blocked_by_ids = list(user.blocked_by.all().values_list(flat=True))
        blocked_profile_ids = list(
            user.profile.blocked_profiles.all().values_list(flat=True)
        )
        block_list_ids = blocked_by_ids + blocked_profile_ids

        search_term = self.request.query_params.get("searchTerm")
        h_instance = HashTag.objects.get(hashtag=search_term)
        queryset = Item.objects.filter(Q(hashtags=h_instance)).exclude(
            Q(user__in=block_list_ids)
        )
        return queryset

    def get_serializer(self, *args, **kwargs):
        serializer_class = self.get_serializer_class()
        return serializer_class(*args, **kwargs)

    def get_serializer_class(self):
        return ItemDetailSerializer


class LikeUnlikeItemView(APIView):
    def post(self, request, *args, **kwargs):
        item_id = request.data.get("post_id")
        data = {"item": item_id, "user": request.user.id}
        serializer = LikeSerializer(data=data)
        if serializer.is_valid():
            serializer.save()

            # send push notification
            if serializer.instance.user != serializer.instance.item.user:
                send_item_like_notification.delay(
                    receiver_id=serializer.instance.item.user.id,
                    sender_id=serializer.instance.user.id,
                )

            return Response(status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, *args, **kwargs):
        item_id = request.query_params.get("post_id")
        user_id = request.user.id
        like_instance = Like.objects.get(item=item_id, user=user_id)
        like_instance.delete()

        item = Item.objects.get(id=item_id)
        item_user = User.objects.get(id=item.user.id)
        item_user.profile.total_likes = F("total_likes") - 1
        item_user.profile.save()
        item_user.save()
        return Response(status=status.HTTP_204_NO_CONTENT)


class CheckItemLikeView(APIView):
    def get(self, request, *args, **kwargs):
        item_id = request.query_params.get("post_id")
        user_id = request.user.id
        if Like.objects.filter(item=item_id, user=user_id).exists():
            return Response({"liked": True}, status=status.HTTP_200_OK)
        return Response({"liked": False}, status=status.HTTP_200_OK)


class ItemDeleteView(APIView):
    permission_classes = [IsOwnerOrAdmin]

    def delete(self, request, *args, **kwargs):
        item_id = request.query_params.get("post_id")
        delete_item.delay(item_id)
        return Response(status=status.HTTP_204_NO_CONTENT)


class ItemLikedUsersView(generics.ListAPIView):
    pagination_class = PostLikedUserPagination

    def get_queryset(self):
        post_id = self.request.query_params.get("postId")
        item_instance = Item.objects.get(id=post_id)
        queryset = Like.objects.filter(item=item_instance)
        return queryset

    def get_serializer(self, *args, **kwargs):
        serializer_class = self.get_serializer_class()
        return serializer_class(*args, **kwargs)

    def get_serializer_class(self):
        return ItemLikedUserSerializer


class ReportItemView(APIView):
    def post(self, request, *args, **kwargs):
        item_id = request.data.get("post_id")
        item = Item.objects.get(id=item_id)
        item.report_counter = F("report_counter") + 1
        item.save()
        return Response(status=status.HTTP_201_CREATED)


# s3 signature to direct upload from Frontend
class AwsS3SignatureAPI(APIView):
    permission_classes = [IsOwnerOrAdmin]

    def get(self, request, *args, **kwargs):
        file_name = request.query_params.get("fileName")
        s3 = boto3.client("s3", "us-east-2", config=Config(signature_version="s3v4"))
        s3_params = {
            "Bucket": settings.AWS_STORAGE_BUCKET_NAME,
            # "Bucket": "storyfeed-production-bucket",
            "Key": f"{default_storage.location}/{file_name}",
        }
        presigned_url = s3.generate_presigned_url(
            "put_object", Params=s3_params, ExpiresIn=3600, HttpMethod="PUT"
        )
        return Response({"presigned_url": presigned_url}, status=status.HTTP_200_OK)
