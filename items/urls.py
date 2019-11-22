from django.urls import path

from .views import ItemCreateView, ItemListView

urlpatterns = [
    path("upload/", ItemCreateView.as_view(), name="upload_post"),
    path("user/", ItemListView.as_view(), name="user_posts"),
]

