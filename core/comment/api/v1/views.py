from rest_framework.permissions import IsAuthenticated
from .serializers import CommentSerializer
from comment.models import Comment
from django.contrib.auth import get_user_model
from rest_framework import viewsets
from rest_framework.exceptions import PermissionDenied


User = get_user_model()


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated]
    ordering_fields = ["created_date"]

    def get_queryset(self):
        if not self.request.user.is_authenticated:
            raise PermissionDenied("You must be logged in to view your comments.")
        return super().get_queryset().filter(author=self.request.user.profile)

    def perform_create(self, serializer):
        if not self.request.user.is_authenticated:
            raise PermissionDenied("You must be logged in to create a comment.")
        serializer.save(author=self.request.user.profile)
