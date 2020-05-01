from django.urls import path

from .views import (
    CheckUserExistsAPI,
    CheckEmailExistsAPI,
    RegisterAPI,
    LoginAPI,
    LogoutAPI,
    ChangePasswordAPI,
    DeleteUserAPI,
)

urlpatterns = [
    path(
        "check-user-exists/", CheckUserExistsAPI.as_view(), name="chek_if_user_exists"
    ),
    path(
        "check-email-exists/",
        CheckEmailExistsAPI.as_view(),
        name="check_if_email_exists",
    ),
    path("register/", RegisterAPI.as_view(), name="register"),
    path("login/", LoginAPI.as_view(), name="login"),
    path("logout/", LogoutAPI.as_view(), name="logout"),
    path("change-password/", ChangePasswordAPI.as_view(), name="change_password"),
    path("delete-user/", DeleteUserAPI.as_view(), name="delete_user_account"),
]
