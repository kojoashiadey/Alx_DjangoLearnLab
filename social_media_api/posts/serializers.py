
# posts/serializers.py
from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Post, Comment, Like

User = get_user_model()

class UserBriefSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("id", "username")

class CommentSerializer(serializers.ModelSerializer):
    author = UserBriefSerializer(read_only=True)
    author_id = serializers.IntegerField(write_only=True, required=False)

    class Meta:
        model = Comment
        fields = ("id", "post", "post_id", "author", "author_id", "content", "created_at", "updated_at")
        read_only_fields = ("id", "created_at", "updated_at", "author")

    def create(self, validated_data):
        # If client provides author_id ensure it is used, otherwise view will set author
        author_id = validated_data.pop("author_id", None)
        if author_id:
            # Use direct creation (assumes valid id)
            return Comment.objects.create(author_id=author_id, **validated_data)
        return Comment.objects.create(**validated_data)

class PostSerializer(serializers.ModelSerializer):
    author = UserBriefSerializer(read_only=True)
    author_id = serializers.IntegerField(write_only=True, required=False)
    comments = CommentSerializer(read_only=True, many=True)
    comments_count = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = ("id", "author", "author_id", "title", "content", "created_at", "updated_at", "comments", "comments_count")
        read_only_fields = ("id", "created_at", "updated_at", "author", "comments")

    def get_comments_count(self, obj):
        return obj.comments.count()

    def create(self, validated_data):
        author_id = validated_data.pop("author_id", None)
        if author_id:
            return Post.objects.create(author_id=author_id, **validated_data)
        return Post.objects.create(**validated_data)


class LikeSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Like
        fields = ("id", "post", "user", "created_at")
        read_only_fields = ("id", "user", "created_at")
