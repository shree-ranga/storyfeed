from django.urls import path

from .views import PostCreateView, PostListView

urlpatterns = [
    path("upload/", PostCreateView.as_view(), name="upload_post"),
    path("user/", PostListView.as_view(), name="user_posts"),
]

