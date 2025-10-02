from django.urls import path, include
from . import views

app_name = "comment"

urlpatterns = [
    path(
        "post/<int:post_id>/comments/",
        views.CommentListView.as_view(),
        name="comment-list",
    ),
    path(
        "post/<int:post_id>/create/",
        views.CommentCreateView.as_view(),
        name="comment-create",
    ),
    path(
        "comment/<int:post_id>/edit/<int:pk>/",
        views.CommentEditView.as_view(),
        name="comment-edit",
    ),
    path(
        "comment/<int:post_id>/delete/<int:pk>/",
        views.CommentDeleteView.as_view(),
        name="comment-delete",
    ),
    path("api/v1/", include("comment.api.v1.urls")),
]
