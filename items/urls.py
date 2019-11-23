from django.urls import path

from .views import ItemCreateView, ItemListView, UserFeedView

urlpatterns = [
    path("upload/", ItemCreateView.as_view(), name="upload_post"),
    path("user/", ItemListView.as_view(), name="user_posts"),
    path("feed/", UserFeedView.as_view(), name="user_feed"),
]

