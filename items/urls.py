from django.urls import path

from .views import (
    ItemCreateView,
    ItemListView,
    UserFeedView,
    LikeView,
    UnlikeView,
    CheckLike,
    LikedItemView,
)

urlpatterns = [
    path("upload/", ItemCreateView.as_view(), name="upload_post"),
    path("user/", ItemListView.as_view(), name="user_posts"),
    path("feed/", UserFeedView.as_view(), name="user_feed"),
    path("like/", LikeView.as_view(), name="post_like"),
    path("unlike/", UnlikeView.as_view(), name="post_unlike"),
    path("check-like/", CheckLike.as_view(), name="check_post_like"),
    path("liked-items/", LikedItemView.as_view(), name="liked_posts"),
]

