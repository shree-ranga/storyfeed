import os
import datetime
from io import BytesIO

from django.db.models import F
from django.contrib.auth import get_user_model
from django.core.files.base import ContentFile

from rest_framework.views import APIView
from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import ValidationError

from PIL import Image

from .models import Item, Like
from .serializers import (
    ItemCreateSerializer,
    ItemListSerializer,
    ItemDetailSerializer,
    LikeSerializer,
)
from .pagination import (
    UserItemListPagination,
    SearchItemListPagination,
    FeedPagination,
)
from .permissions import IsOwnerOrAdmin

from notifications.serializers import NotificationSerializer

from items.tasks import delete_after_expiration, send_item_like_notification


class ItemCreateView(APIView):
    def post(self, request, *args, **kwargs):
        item = self.request.data.get("item")
        expiration_time = self.request.data.pop("expiration_time")
        serializer = ItemCreateSerializer(data={"item": item})
        if serializer.is_valid():
            serializer.save(user=request.user)
            if expiration_time[0] == "1D":
                time_to_delete = serializer.instance.created_at + datetime.timedelta(
                    days=1
                )
            elif expiration_time[0] == "1W":
                time_to_delete = serializer.instance.created_at + datetime.timedelta(
                    days=7
                )
            elif expiration_time[0] == "1Y":
                time_to_delete = serializer.instance.created_at + datetime.timedelta(
                    days=365
                )
            delete_after_expiration.apply_async(
                args=(serializer.instance.id,), eta=time_to_delete
            )
            return Response(
                {"msg": "Upload item successful..."}, status=status.HTTP_200_OK
            )
        print(serializer.errors)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# TODO: - refactor. Change query params to args
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
    pagination_class = SearchItemListPagination

    def get_queryset(self):
        user = self.request.user
        following_ids = list(user.profile.following.all().values_list(flat=True))
        following_ids.append(user.id)
        queryset = Item.objects.exclude(user__in=following_ids)
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


class LikeItemView(APIView):
    def post(self, request, *args, **kwargs):
        item_id = request.data.get("post_id")
        data = {"item": item_id}
        serializer = LikeSerializer(data=data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            if serializer.instance.user != serializer.instance.item.user:
                notification_data = {
                    "receiver": serializer.instance.item.user.id,
                    "sender": serializer.instance.user.id,
                    "content_object": serializer.instance,
                    "notification_type": "like",
                }
                notification_serializer = NotificationSerializer(data=notification_data)
                if notification_serializer.is_valid():
                    notification_serializer.save()
                    send_item_like_notification.delay(
                        receiver_id=notification_serializer.instance.receiver_id,
                        sender_id=notification_serializer.instance.sender_id,
                    )
                # else:
                #     return "Could not save notification object"
            return Response({"msg": "Like created..."}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UnlikeItemView(APIView):
    def post(self, request, *args, **kwargs):
        item_id = request.data.get("post_id")
        user_id = request.user.id
        like_instance = Like.objects.get(item=item_id, user=user_id)
        like_instance.delete()
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
    # TODO: - make this a celery task
    def delete(self, request, *args, **kwargs):
        item_id = request.query_params.get("post_id")
        item = Item.objects.get(id=item_id)
        item.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class ReportItemView(APIView):
    # TODO: - run a periodic task to monitor reports
    def post(self, request, *args, **kwargs):
        item_id = request.data.get("post_id")
        item = Item.objects.get(id=item_id)
        item.report_counter += 1
        item.save()
        return Response(status=status.HTTP_201_CREATED)


# class to direct upload from Frontend
class AwsS3SignatureAPI(APIView):
    pass
