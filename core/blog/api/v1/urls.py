from .views import BlogViewSet, CategoryModelViewSet
from rest_framework.routers import DefaultRouter

app_name = "api-v1"

router = DefaultRouter()
router.register("post", BlogViewSet, basename="post"),
router.register("category", CategoryModelViewSet, basename="category")

urlpatterns = router.urls
