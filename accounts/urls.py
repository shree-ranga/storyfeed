from django.urls import path

from .views import (
    UserListAPI,
    UserDetailAPI,
    UploadProfileAvatarAPI,
    FollowUnfollowAPI,
    CheckFollowedAPI,
)

urlpatterns = [
    path("users/", UserListAPI.as_view(), name="user_list"),
    path("users/<int:pk>/", UserDetailAPI.as_view(), name="user_detail"),
    path(
        "users/profile/avatar/", UploadProfileAvatarAPI.as_view(), name="profile_avatar"
    ),
    path(
        "users/follow_unfollow/",
        FollowUnfollowAPI.as_view(),
        name="user_follow_unfollow",
    ),
    path("users/check_followed/", CheckFollowedAPI.as_view(), name="check_followed"),
]
