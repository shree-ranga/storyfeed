import datetime

from django.db.models import F, Q
from django.contrib.auth import get_user_model
from django.conf import settings

from rest_framework.views import APIView
from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status

import boto3

from .models import Item, Like
from .serializers import (
    ItemCreateSerializer,
    ItemListSerializer,
    ItemDetailSerializer,
    LikeSerializer,
)
from .pagination import (
    UserItemListPagination,
    ExploreItemListPagination,
    FeedPagination,
)
from .permissions import IsOwnerOrAdmin
from .tasks import delete_item, send_item_like_notification

from notifications.serializers import NotificationSerializer

User = get_user_model()


class ItemCreateView(APIView):
    def post(self, request, *args, **kwargs):
        item = request.data.get("item")
        video_url = request.data.get("video_url")
        expiration_time = request.data.get("expiry_time")
        caption = request.data.get("caption")
        data = {
            "item": item,
            "video_url": video_url,
            "expiry_time": int(expiration_time),
            "caption": caption,
        }
        serializer = ItemCreateSerializer(data=data)
        if serializer.is_valid():
            serializer.save(user=request.user)

            delete_eta = serializer.instance.created_at + datetime.timedelta(
                days=serializer.instance.expiry_time
            )
            delete_item.apply_async(args=(serializer.instance.id,), eta=delete_eta)

            return Response(status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserItemListDetailView(generics.ListAPIView):
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


class ExploreItemsView(generics.ListAPIView):
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


class UserFeedView(generics.ListAPIView):
    pagination_class = FeedPagination

    def get_queryset(self):
        user = self.request.user
        following_ids = list(user.profile.following.all().values_list(flat=True))
        following_ids.append(user.id)
        queryset = Item.objects.filter(user__in=following_ids)
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
        s3 = boto3.client("s3")
        s3_params = {
            "Bucket": settings.AWS_STORAGE_BUCKET_NAME,
            "Key": f"media/{file_name}",
        }
        presigned_url = s3.generate_presigned_url(
            "put_object", Params=s3_params, ExpiresIn=3600, HttpMethod="PUT"
        )
        return Response({"presigned_url": presigned_url}, status=status.HTTP_200_OK)
