from django.urls import path

from .views import RegisterAPI, LoginAPI, LogoutAPI, CheckUserExistsAPI

urlpatterns = [
    path(
        "check-user-exists/", CheckUserExistsAPI.as_view(), name="chek_if_user_exists"
    ),
    path("register/", RegisterAPI.as_view(), name="register"),
    path("login/", LoginAPI.as_view(), name="login"),
    path("logout/", LogoutAPI.as_view(), name="logout"),
]

