from rest_framework.permissions import IsAuthenticated
from .serializers import BlogSerializer, CategorySerializer
from blog.models import Post, Category
from django.contrib.auth import get_user_model
from rest_framework import viewsets
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.exceptions import PermissionDenied


User = get_user_model()


class BlogViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = BlogSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ["category"]
    search_fields = ["title"]
    ordering_fields = ["created_date"]

    def get_queryset(self):
        if not self.request.user.is_authenticated:
            raise PermissionDenied("You must be logged in to view your posts.")
        return super().get_queryset().filter(author=self.request.user.profile)

    def perform_create(self, serializer):
        if not self.request.user.is_authenticated:
            raise PermissionDenied("You must be logged in to create a post.")
        serializer.save(author=self.request.user.profile)


class CategoryModelViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = CategorySerializer
    queryset = Category.objects.all()
