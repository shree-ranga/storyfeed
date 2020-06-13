from django.urls import path

from .views import (
    ItemCreateView,
    UserItemListDetailView,
    ExploreItemsView,
    UserFeedView,
    LikeUnlikeItemView,
    CheckItemLikeView,
    ItemDeleteView,
)

urlpatterns = [
    path("upload/", ItemCreateView.as_view(), name="upload_post"),
    path("user/", UserItemListDetailView.as_view(), name="user_posts"),
    path("explore-items/", ExploreItemsView.as_view(), name="explorable_items"),
    path("feed/", UserFeedView.as_view(), name="user_feed"),
    path("like-unlike/", LikeUnlikeItemView.as_view(), name="post_like_unlike"),
    path("check-like/", CheckItemLikeView.as_view(), name="check_post_like"),
    path("delete/", ItemDeleteView.as_view(), name="delete"),
]
