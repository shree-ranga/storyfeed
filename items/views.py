from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import ValidationError

from .models import Item
from .serializers import ItemSerializer


class PostCreateView(APIView):
    def post(self, request, *args, **kwargs):
        item = request.data.get("item")
        caption = request.data.get("caption", None)
        data = {"item": item}
        if caption is not None:
            data["caption"] = caption
        serializer = ItemSerializer(data=data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(
                {"msg": "Upload item successful..."}, status=status.HTTP_201_CREATED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PostListView(APIView):
    def get(self, request, *args, **kwargs):
        return Response({"msg": "list_post"}, status=status.HTTP_200_OK)
