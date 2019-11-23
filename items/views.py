from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import ValidationError

from .models import Item
from .serializers import ItemCreateSerializer, ItemListSerializer, ItemDetailSerializer


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


class UserFeedView(APIView):
    def get(self, request, *args, **kwargs):
        user = request.user
        user_id = user.id
        following_ids = list(user.profile.following.all().values_list(flat=True))
        following_ids.append(user_id)
        queryset = Item.objects.filter(user__in=following_ids)
        serializer = ItemDetailSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
