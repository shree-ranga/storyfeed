from rest_framework import generics

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
