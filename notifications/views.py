from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .models import Notification
from .serializers import NotificationSerializer


class NotificationListView(APIView):
    def get(self, request, *args, **kwargs):
        queryset = Notification.objects.filter(receiver=request.user)
        serializer = NotificationSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
