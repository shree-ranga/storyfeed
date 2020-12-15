from django.urls import path

from .views import (
    ItemCreateView,
    UpdateEngagementCounterView,
    ProfileItemListView,
    ExploreItemsListView,
    FeedItemsListView,
    HashTagItemListView,
    LikeUnlikeItemView,
    CheckItemLikeView,
    ItemDeleteView,
    ReportItemView,
    AwsS3SignatureAPI,
    ItemLikedUsersView,
)

urlpatterns = [
    path("upload/", ItemCreateView.as_view(), name="upload_post"),
    path(
        "update-engagement/",
        UpdateEngagementCounterView.as_view(),
        name="update engagement",
    ),
    path("user/", ProfileItemListView.as_view(), name="user_posts"),
    path("liked-users/", ItemLikedUsersView.as_view(), name="liked_users"),
    path("explore-items/", ExploreItemsListView.as_view(), name="explorable_items"),
    path("hashtag-items/", HashTagItemListView.as_view(), name="hashtag-items"),
    path("feed/", FeedItemsListView.as_view(), name="user_feed"),
    path("like-unlike/", LikeUnlikeItemView.as_view(), name="post_like_unlike"),
    path("check-like/", CheckItemLikeView.as_view(), name="check_post_like"),
    path("delete/", ItemDeleteView.as_view(), name="delete"),
    path("report/", ReportItemView.as_view(), name="report"),
    path("aws-s3-direct/", AwsS3SignatureAPI.as_view(), name="AWS_S3_direct"),
]
