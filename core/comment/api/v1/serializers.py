from rest_framework import serializers
from comment.models import Comment


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ["id", "content", "author", "post"]
        read_only_fields = [
            "author",
        ]

    def create(self, validated_data):
        author = self.context["request"].user.profile
        if not author.is_verified:
            raise serializers.ValidationError("Only verified users can create comment.")
        validated_data["author"] = author
        return super().create(validated_data)
