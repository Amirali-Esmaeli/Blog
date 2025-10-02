from rest_framework import serializers
from blog.models import Post, Category


class BlogSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = [
            "id",
            "title",
            "content",
            "status",
            "category",
            "published_date",
        ]
        read_only_fields = ["author"]

    def create(self, validated_data):
        author = self.context["request"].user.profile
        if not author.user.is_verified:
            raise serializers.ValidationError("Only verified users can create post.")
        validated_data["author"] = author
        return super().create(validated_data)


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = ["name", "id"]

    def create(self, validated_data):
        author = self.context["request"].user.profile
        if not author.user.is_verified:
            raise serializers.ValidationError(
                "Only verified users can create category."
            )
        validated_data["author"] = author
        return super().create(validated_data)
