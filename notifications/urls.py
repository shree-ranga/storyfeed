from django.urls import path

from push_notifications.api.rest_framework import APNSDeviceAuthorizedViewSet

from .views import (
    NotificationListView,
    CheckNotificationStatus,
    SetNotificationsCheckedAPI,
)

# in-app notification urls
urlpatterns = [
    path(
        "user-notifications/", NotificationListView.as_view(), name="user_notifications"
    ),
    path(
        "check-status/",
        CheckNotificationStatus.as_view(),
        name="check_notification_status",
    ),
    path(
        "set-check/",
        SetNotificationsCheckedAPI.as_view(),
        name="set_notification_checked",
    ),
]

# push notification urls
urlpatterns += [
    path(
        "push-notifications/device/apns/",
        APNSDeviceAuthorizedViewSet.as_view({"post": "create"}),
        name="create_apns_device",
    )
]
