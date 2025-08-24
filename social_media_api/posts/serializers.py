from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Post, Comment

User = get_user_model()

class UserMiniSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username"]

class CommentSerializer(serializers.ModelSerializer):
    author = UserMiniSerializer(read_only=True)
    author_id = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(), source="author", write_only=True, required=False
    )

    class Meta:
        model = Comment
        fields = ["id", "post", "author", "author_id", "content", "created_at", "updated_at"]
        read_only_fields = ["id", "author", "created_at", "updated_at"]

    def create(self, validated_data):
        # Prefer authenticated user; fallback to author_id if explicitly provided
        request = self.context.get("request")
        if request and request.user and request.user.is_authenticated:
            validated_data["author"] = request.user
        return super().create(validated_data)


class PostSerializer(serializers.ModelSerializer):
    author = UserMiniSerializer(read_only=True)
    author_id = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(), source="author", write_only=True, required=False
    )
    comments_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = Post
        fields = [
            "id", "author", "author_id", "title", "content",
            "created_at", "updated_at", "comments_count"
        ]
        read_only_fields = ["id", "author", "created_at", "updated_at", "comments_count"]

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data["comments_count"] = instance.comments.count()
        return data

    def create(self, validated_data):
        request = self.context.get("request")
        if request and request.user and request.user.is_authenticated:
            validated_data["author"] = request.user
        return super().create(validated_data)
