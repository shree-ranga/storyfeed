import datetime
import calendar

from django.db.models import F
from django.contrib.auth import get_user_model
from django.conf import settings

from rest_framework.views import APIView
from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status

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
from .tasks import send_item_like_notification, delete_item

from notifications.serializers import NotificationSerializer

from storyboard.storage_backends import MediaStorage

User = get_user_model()


class ItemCreateView(APIView):
    def post(self, request, *args, **kwargs):
        item = request.data.get("item")
        expiration_time = request.data.pop("expiration_time")

        serializer = ItemCreateSerializer(data={"item": item})
        if serializer.is_valid():
            serializer.save(user=request.user)

            created_at = serializer.instance.created_at
            if expiration_time[0] == "1D":
                time_to_delete = created_at + datetime.timedelta(days=1)
            elif expiration_time[0] == "1M":
                time_to_delete = created_at + datetime.timedelta(days=7)
            elif expiration_time[0] == "1Y":
                if calendar.isleap(datetime.datetime.now().year):
                    time_to_delete = created_at + datetime.timedelta(days=366)
                else:
                    time_to_delete = created_at + datetime.timedelta(days=365)
            delete_item.apply_async(args=(serializer.instance.id,), eta=time_to_delete)

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


class LikeUnlikeItemView(APIView):
    def post(self, request, *args, **kwargs):
        item_id = request.data.get("post_id")
        data = {"item": item_id}

        serializer = LikeSerializer(data=data)
        if serializer.is_valid():
            serializer.save(user=request.user)

            user = User.objects.get(id=serializer.instance.item.user.id)
            user.profile.total_likes += 1
            user.profile.save()
            user.save()

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
            return Response(status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, *args, **kwargs):
        item_id = request.query_params.get("post_id")
        user_id = request.user.id

        item = Item.objects.get(id=item_id)
        item_user = User.objects.get(id=item.user.id)
        item_user.profile.total_likes -= 1
        item_user.profile.save()
        item_user.save()

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

    def delete(self, request, *args, **kwargs):
        item_id = request.query_params.get("post_id")
        delete_item.delay(item_id)
        return Response(status=status.HTTP_204_NO_CONTENT)


class ReportItemView(APIView):
    def post(self, request, *args, **kwargs):
        item_id = request.data.get("post_id")
        item = Item.objects.get(id=item_id)
        item.report_counter += 1
        item.save()
        return Response(status=status.HTTP_201_CREATED)


# s3 signature to direct upload from Frontend
class AwsS3SignatureAPI(APIView):
    pass
