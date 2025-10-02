from celery import shared_task
from .models import Post


@shared_task
def delete_posts():
    deleted_count, _ = Post.objects.filter(status=True).delete()
    print(f"{deleted_count}  posts deleted")
    return f"{deleted_count} posts deleted"
