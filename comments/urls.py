from django.urls import path

from .views import CommentCreateView, CommentListView

urlpatterns = [
    path("create/", CommentCreateView.as_view(), name="create_comment"),
    path("item-comments/", CommentListView.as_view(), name="item_comments"),
]

