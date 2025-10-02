from django.shortcuts import render
from blog.models import Post
from .models import Comment
from .forms import CommentForm
from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.views.generic import ListView, CreateView, UpdateView, DeleteView

# Create your views here.


class CommentListView(ListView):
    model = Comment
    context_object_name = "comments"

    def get_queryset(self):
        post_id = self.kwargs["post_id"]
        return Comment.objects.filter(post_id=post_id)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["post"] = get_object_or_404(Post, pk=self.kwargs["post_id"])
        return context


class CommentCreateView(CreateView):
    model = Comment
    form_class = CommentForm

    def form_valid(self, form):
        form.instance.author = self.request.user.profile
        form.instance.post_id = self.kwargs["post_id"]
        return super().form_valid(form)

    def get_success_url(self):
        return reverse(
            "comment:comment-list", kwargs={"post_id": self.kwargs["post_id"]}
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["post"] = get_object_or_404(Post, pk=self.kwargs["post_id"])
        return context


class CommentEditView(UpdateView):
    model = Comment
    form_class = CommentForm

    def get_success_url(self):
        return reverse(
            "comment:comment-list", kwargs={"post_id": self.kwargs["post_id"]}
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["post"] = get_object_or_404(Post, pk=self.kwargs["post_id"])
        return context


class CommentDeleteView(DeleteView):
    model = Comment

    def get_success_url(self):
        return reverse(
            "comment:comment-list", kwargs={"post_id": self.kwargs["post_id"]}
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["post"] = get_object_or_404(Post, pk=self.kwargs["post_id"])
        return context
