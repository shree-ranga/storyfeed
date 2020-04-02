from rest_framework.views import APIView
from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import ValidationError

from .models import Comment
from .serializers import CommentCreateSerializer, CommentListSerializer
from .pagination import CommentPagination

from notifications.serializers import NotificationSerializer


class CommentCreateView(APIView):
    def post(self, request, *args, **kwargs):
        item_id = request.data.get("post_id")
        comment = request.data.get("comment")
        data = {"comment": comment, "item": item_id}
        serializer = CommentCreateSerializer(data=data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            if serializer.instance.user != serializer.instance.item.user:
                notification_data = {
                    "receiver": serializer.instance.item.user.id,
                    "sender": serializer.instance.user.id,
                    "content_object": serializer.instance,
                    "notification_type": "comment",
                }
                notification_serializer = NotificationSerializer(data=notification_data)
                if notification_serializer.is_valid():
                    notification_serializer.save()
                else:
                    return "Could not save notification object"
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CommentListView(generics.ListAPIView):
    pagination_class = CommentPagination

    def get_queryset(self):
        item_id = self.request.query_params.get("post_id")
        comments = Comment.objects.filter(item__id=item_id)
        return comments

    def get_serializer(self, *args, **kwargs):
        serializer_class = self.get_serializer_class()
        return serializer_class(*args, **kwargs)

    def get_serializer_class(self):
        return CommentListSerializer

    # def get(self, request, *args, **kwargs):
    #     item_id = request.query_params.get("post_id")
    #     queryset = self.get_queryset(id=item_id)
    #     if queryset:
    #         serializer = CommentListSerializer(queryset, many=True)
    #         return Response(serializer.data, status=status.HTTP_200_OK)
    #     return Response(status=status.HTTP_404_NOT_FOUND)
