from django.urls import path

from .views import NotificationListView

urlpatterns = [
    path(
        "user-notifications/", NotificationListView.as_view(), name="user_notifications"
    )
]

