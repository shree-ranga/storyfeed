from django.urls import path

from .views import (
    ItemCreateView,
    UserItemListDetailView,
    AllItemsView,
    UserFeedView,
    LikeItemView,
    UnlikeItemView,
    CheckItemLikeView,
)

urlpatterns = [
    path("upload/", ItemCreateView.as_view(), name="upload_post"),
    path("user/", UserItemListDetailView.as_view(), name="user_posts"),
    path("all-items/", AllItemsView.as_view(), name="get_all_items"),
    path("feed/", UserFeedView.as_view(), name="user_feed"),
    path("like/", LikeItemView.as_view(), name="post_like"),
    path("unlike/", UnlikeItemView.as_view(), name="post_unlike"),
    path("check-like/", CheckItemLikeView.as_view(), name="check_post_like"),
]
