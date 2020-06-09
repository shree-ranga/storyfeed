from django.urls import path

from .views import CommentCreateView, CommentListView, CommentDeleteView

urlpatterns = [
    path("create/", CommentCreateView.as_view(), name="create_comment"),
    path("item-comments/", CommentListView.as_view(), name="item_comments"),
    path("delete/", CommentDeleteView.as_view(), name="delete_comment"),
]
