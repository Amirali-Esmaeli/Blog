from rest_framework.test import APIClient
from django.urls import reverse
import pytest
from accounts.models import User
from ..models import Post, Category


@pytest.fixture
def api_client():
    client = APIClient()
    return client


@pytest.fixture
def common_user():
    user = User.objects.create_user(
        email="tests@tests.com", password="Amirali83!", is_verified=True
    )
    return user


@pytest.fixture
def unverified_user():
    user = User.objects.create_user(
        email="notverified@example.com",
        password="Test1234!",
        is_verified=False,
    )
    return user


@pytest.fixture
def user_category():
    return Category.objects.create(
        name="category",
    )


@pytest.fixture
def user_post(common_user, user_category):
    return Post.objects.create(
        title="My post",
        content="content",
        status=True,
        category=user_category,
        published_date="2025-09-28T11:59:23.086Z",
        author=common_user.profile,
    )


@pytest.fixture
def another_verified_user(db):
    return User.objects.create_user(
        email="another@example.com", password="Test1234!", is_verified=True
    )


@pytest.mark.django_db
class TestBlogApi:

    def test_get_post_response_200_status(self, api_client, common_user):
        url = reverse("blog:api-v1:post-list")
        user = common_user
        api_client.force_login(user=user)
        response = api_client.get(url)
        assert response.status_code == 200

    def test_get_post_response_401_status(self, api_client):
        url = reverse("blog:api-v1:post-list")
        response = api_client.get(url)
        assert response.status_code == 401

    def test_create_post_response_201_status(self, api_client, common_user):
        url = reverse("blog:api-v1:post-list")
        data = {
            "title": "test",
            "content": "content",
            "status": True,
            "published_date": "2025-09-28T11:59:23.086Z",
        }
        user = common_user
        api_client.force_login(user=user)
        response = api_client.post(url, data)
        assert response.status_code == 201
        assert response.data["title"] == data["title"]

    def test_create_post_response_401_status(self, api_client):
        url = reverse("blog:api-v1:post-list")
        data = {
            "title": "test",
            "content": "content",
            "status": True,
            "published_date": "2025-09-28T11:59:23.086Z",
        }
        response = api_client.post(url, data)
        assert response.status_code == 401

    def test_create_post_invalid_data_response_400_status(
        self, api_client, common_user
    ):
        url = reverse("blog:api-v1:post-list")
        data = {}
        user = common_user
        api_client.force_login(user=user)
        response = api_client.post(url, data)
        assert response.status_code == 400

    def test_unverified_user_cannot_create_post(self, api_client, unverified_user):
        api_client.force_login(user=unverified_user)
        url = reverse("blog:api-v1:post-list")
        data = {
            "title": "New Task",
            "content": "content",
            "status": True,
            "published_date": "2025-09-28T11:59:23.086Z",
        }
        response = api_client.post(url, data)
        assert response.status_code == 400

    def test_verified_user_can_edit_own_post(self, api_client, common_user, user_post):
        api_client.force_login(user=common_user)
        url = reverse("blog:api-v1:post-detail", kwargs={"pk": user_post.pk})
        data = {"title": "Updated Task"}
        response = api_client.patch(url, data)
        assert response.status_code == 200
        assert response.data["title"] == data["title"]

    def test_verified_user_cannot_edit_others_post(
        self, api_client, another_verified_user, user_post
    ):
        api_client.force_login(user=another_verified_user)
        url = reverse("blog:api-v1:post-detail", kwargs={"pk": user_post.pk})
        data = {"title": "Hacked Task"}
        response = api_client.patch(url, data)
        assert response.status_code == 404

    def test_verified_user_can_delete_own_post(
        self, api_client, common_user, user_post
    ):
        api_client.force_login(user=common_user)
        url = reverse("blog:api-v1:post-detail", kwargs={"pk": user_post.pk})
        response = api_client.delete(url)
        assert response.status_code == 204

    def test_verified_user_cannot_delete_others_post(
        self, api_client, another_verified_user, user_post
    ):
        api_client.force_login(user=another_verified_user)
        url = reverse("blog:api-v1:post-detail", kwargs={"pk": user_post.pk})
        response = api_client.delete(url)
        assert response.status_code == 404
