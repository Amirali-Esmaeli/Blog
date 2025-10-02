from django.db import models
from django.contrib.auth import get_user_model
from blog.models import Post

# Create your models here.

# getting user model object
# User = get_user_model()


class Comment(models.Model):
    author = models.ForeignKey("accounts.Profile", on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    content = models.TextField()
    created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"comment-author: {self.author.user.email} - post: {self.post}"
