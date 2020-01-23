from django.urls import path

from push_notifications.api.rest_framework import APNSDeviceAuthorizedViewSet

from .views import NotificationListView

# in-app notification urls
urlpatterns = [
    path(
        "user-notifications/", NotificationListView.as_view(), name="user_notifications"
    )
]

# push notification urls
urlpatterns += [
    path(
        "push-notifications/device/apns/",
        APNSDeviceAuthorizedViewSet.as_view({"post": "create"}),
        name="create_apns_device",
    )
]
