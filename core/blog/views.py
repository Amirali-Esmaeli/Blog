from django.shortcuts import render
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView,
)
from .models import Post
from .forms import PostForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page

# Create your views here.


@method_decorator(cache_page(60 * 20), name="dispatch")
class PostListView(LoginRequiredMixin, ListView):
    model = Post
    context_object_name = "posts"
    paginate_by = 3
    ordering = "id"

    def get_queryset(self):
        return Post.objects.filter(author=self.request.user.profile)


class PostDetailView(LoginRequiredMixin, DetailView):
    model = Post
    context_object_name = "post"


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    form_class = PostForm
    success_url = "/blog/post/"

    def form_valid(self, form):
        form.instance.author = self.request.user.profile
        return super().form_valid(form)


class PostEditView(LoginRequiredMixin, UpdateView):
    model = Post
    form_class = PostForm
    success_url = "/blog/post/"


class PostDeleteView(LoginRequiredMixin, DeleteView):
    model = Post
    success_url = "/blog/post/"
