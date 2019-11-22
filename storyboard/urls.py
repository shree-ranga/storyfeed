from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings

api_v1 = "api/v1/"

urlpatterns = [
    path("admin/", admin.site.urls),
    path(api_v1 + "dummy/", include("play.urls")),
    path(api_v1 + "accounts/", include("accounts.urls")),
    path(api_v1 + "accounts/auth/", include("accounts.auth.urls")),
    path(api_v1 + "items/", include("items.urls")),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
