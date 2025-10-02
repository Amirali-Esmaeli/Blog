from .views import CommentViewSet
from rest_framework.routers import DefaultRouter

app_name = "api-v1"

router = DefaultRouter()
router.register("posts/comments", CommentViewSet, basename="comment"),

urlpatterns = router.urls
