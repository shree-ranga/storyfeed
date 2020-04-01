from django.urls import path

from .views import (
    UserListAPI,
    UserDetailAPI,
    UploadProfileAvatarAPI,
    UserFollowUnfollowAPI,
    CheckFollowedAPI,
    UserFollowersListAPI,
    UserFollowingListAPI,
    EditUserView,
)

urlpatterns = [
    path("users/", UserListAPI.as_view(), name="user_list"),
    path("users/<int:pk>/", UserDetailAPI.as_view(), name="user_detail",),
    path(
        "users/profile/avatar/", UploadProfileAvatarAPI.as_view(), name="profile_avatar"
    ),
    path(
        "users/follow_unfollow/",
        UserFollowUnfollowAPI.as_view(),
        name="user_follow_unfollow",
    ),
    path("users/check_followed/", CheckFollowedAPI.as_view(), name="check_followed"),
    path(
        "users/<int:pk>/followers/",
        UserFollowersListAPI.as_view(),
        name="user_followers",
    ),
    path(
        "users/<int:pk>/following/",
        UserFollowingListAPI.as_view(),
        name="user_following",
    ),
    path("users/edit-user/", EditUserView.as_view(), name="edit_user"),
]
