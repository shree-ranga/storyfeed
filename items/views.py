from django.db.models import F

from rest_framework.views import APIView
from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import ValidationError

from .models import Item, Like
from .serializers import (
    ItemCreateSerializer,
    ItemListSerializer,
    ItemDetailSerializer,
    LikeSerializer,
)
from .pagination import UserItemListPagination, SearchItemListPagination, FeedPagination

from notifications.serializers import NotificationSerializer

from .tasks import delete_after_expiration

from datetime import timedelta


class ItemCreateView(APIView):
    def post(self, request, *args, **kwargs):
        item = request.data.get("item")
        expiration_time = request.data.pop("expiration_time")
        data = {"item": item}
        serializer = ItemCreateSerializer(data=data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            if expiration_time[0] == "1 day":
                delete_after_expiration.apply_async(
                    args=(serializer.instance.id,),
                    eta=serializer.instance.created_at + timedelta(seconds=2),
                )
            elif expiration_time[0] == "1 week":
                delete_after_expiration.apply_async(
                    args=(serializer.instance.id,),
                    eta=serializer.instance.created_at + timedelta(seconds=5),
                )
            elif expiration_time[0] == "1 year":
                delete_after_expiration.apply_async(
                    args=(serializer.instance.id,),
                    eta=serializer.instance.created_at + timedelta(seconds=10),
                )
            return Response(
                {"msg": "Upload item successful..."}, status=status.HTTP_201_CREATED
            )
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
        return ItemListSerializer


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
                else:
                    return "Could not save notification object"
            return Response({"msg": "Like created..."}, status=status.HTTP_201_CREATED)
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
    # delete method when user'd like to delete before expiration
    def delete(self, request, *args, **kwargs):
        pass
