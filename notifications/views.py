from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .models import Notification
from .serializers import NotificationListSerializer
from .pagination import NotificationPagination


class NotificationListView(generics.ListAPIView):
    pagination_class = NotificationPagination

    def get_queryset(self):
        notifications = Notification.objects.filter(receiver=self.request.user)
        return notifications

    def get_serializer(self, *args, **kwargs):
        serializer_class = self.get_serializer_class()
        return serializer_class(*args, **kwargs)

    def get_serializer_class(self):
        return NotificationListSerializer


class CheckNotificationStatus(APIView):
    def get(self, request, *args, **kwargs):
        n = Notification.objects.filter(checked=False, receiver=request.user)
        if n.exists():
            return Response({"checked": False}, status=status.HTTP_200_OK)
        else:
            return Response({"checked": True}, status=status.HTTP_200_OK)


class SetNotificationsCheckedAPI(APIView):
    def put(self, request, *args, **kwargs):
        Notification.objects.filter(checked=False, receiver=request.user).update(
            checked=True
        )
        return Response(status=status.HTTP_201_CREATED)
