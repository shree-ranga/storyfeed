from rest_framework.views import APIView
from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import ValidationError

from .models import Comment
from .serializers import CommentCreateSerializer, CommentListSerializer
from .pagination import CommentPagination
from .tasks import send_comment_notification
from .permissions import IsOwnerOrAdmin

from items.models import Item

from notifications.serializers import NotificationSerializer


class CommentCreateView(APIView):
    def post(self, request, *args, **kwargs):
        item_id = request.data.get("post_id")
        comment = request.data.get("comment")
        item = Item.objects.get(id=item_id)
        data = {"comment": comment}
        serializer = CommentCreateSerializer(data=data)
        if serializer.is_valid():
            serializer.save(user=request.user, item=item)

            if serializer.instance.user != serializer.instance.item.user:
                send_comment_notification.delay(
                    receiver_id=serializer.instance.item.user.id,
                    sender_id=serializer.instance.user.id,
                    comment=serializer.instance.comment,
                )
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


class CommentDeleteView(APIView):
    permission_classes = [IsOwnerOrAdmin]

    def delete(self, request, *args, **kwargs):
        comment_id = request.query_params.get("comment_id")
        i = Comment.objects.get(id=comment_id)
        i.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class CommentReportView(APIView):
    pass
