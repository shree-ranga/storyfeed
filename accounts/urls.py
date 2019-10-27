from django.urls import path

from .views import UserListAPI, UserDetailAPI, UploadProfileAvatarAPI

urlpatterns = [
    path("users/", UserListAPI.as_view(), name="user_list"),
    path(
        "users/profile/avatar/", UploadProfileAvatarAPI.as_view(), name="profile_avatar"
    ),
    path("users/<int:pk>/", UserDetailAPI.as_view(), name="user_detail"),
]
