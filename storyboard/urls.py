from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings

# API = "api/v1/"

urlpatterns = [
    path("admin/", admin.site.urls),
    path("dummy/", include("play.urls")),
    path("accounts/", include("accounts.urls")),
    path("accounts/auth/", include("accounts.auth.urls")),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
