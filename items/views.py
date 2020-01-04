from django.db.models import F

from rest_framework.views import APIView
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
from notifications.models import Notification


class ItemCreateView(APIView):
    def post(self, request, *args, **kwargs):
        item = request.data.get("item")
        caption = request.data.get("caption", None)
        data = {"item": item}
        if caption is not None:
            data["caption"] = caption
        serializer = ItemCreateSerializer(data=data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(
                {"msg": "Upload item successful..."}, status=status.HTTP_201_CREATED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ItemListView(APIView):
    def get(self, request, *args, **kwargs):
        user_id = request.query_params.get("uid", None)
        if user_id is not None:
            queryset = Item.objects.filter(user=user_id)
            serializer = ItemListSerializer(queryset, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(
            {"error": "User does not exist"}, status=status.HTTP_400_BAD_REQUEST
        )


class ItemDeleteView(APIView):
    # delete method when user would like to delete before expiration
    def delete(self, request, *args, **kwargs):
        pass


class UserFeedView(APIView):
    def get(self, request, *args, **kwargs):
        user = request.user
        user_id = user.id
        following_ids = list(user.profile.following.all().values_list(flat=True))
        following_ids.append(user_id)
        queryset = Item.objects.filter(user__in=following_ids)
        serializer = ItemDetailSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class LikeView(APIView):
    def post(self, request, *args, **kwargs):
        item_id = request.data.get("post_id")
        data = {"item": item_id}
        serializer = LikeSerializer(data=data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            if serializer.instance.user != serializer.instance.item.user:
                notification = Notification.objects.create(
                    sender=serializer.instance.user,
                    receiver=serializer.instance.item.user,
                    content_object=serializer.instance,
                    notification_type="like",
                )
            return Response({"msg": "Like created..."}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UnlikeView(APIView):
    def post(self, request, *args, **kwargs):
        item_id = request.data.get("post_id")
        user_id = request.user.id
        like_instance = Like.objects.get(item=item_id, user=user_id)
        like_instance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class CheckLike(APIView):
    def get(self, request, *args, **kwargs):
        item_id = request.query_params.get("post_id")
        user_id = request.user.id
        if Like.objects.filter(item=item_id, user=user_id).exists():
            return Response({"liked": True}, status=status.HTTP_200_OK)
        return Response({"liked": False}, status=status.HTTP_200_OK)


class LikedItemView(APIView):
    def get(self, request, *args, **kwargs):
        user_id = request.query_params.get("uid")
        user_liked_items_id = list(
            Like.objects.filter(user=user_id).values_list("item_id", flat=True)
        )
        liked_items = Item.objects.filter(id__in=user_liked_items_id)
        serializer = ItemListSerializer(liked_items, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
