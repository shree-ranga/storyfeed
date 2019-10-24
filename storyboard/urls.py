from django.contrib import admin
from django.urls import path, include

# API = "api/v1/"

urlpatterns = [
    path("admin/", admin.site.urls),
    path("dummy/", include("play.urls")),
    path("accounts/", include("accounts.urls")),
    path("accounts/auth/", include("accounts.auth.urls")),
]
