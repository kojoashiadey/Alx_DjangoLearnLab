from django.contrib.auth import get_user_model
from django.contrib.contenttypes.models import ContentType
from rest_framework import viewsets, permissions, generics, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Post, Comment, Like
from .serializers import PostSerializer, CommentSerializer, LikeSerializer
from notifications.models import Notification

User = get_user_model()


# ---------------------------
# Custom Permission
# ---------------------------
class IsOwnerOrReadOnly(permissions.BasePermission):
    """Allow only owners of an object to edit or delete it."""

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.author == request.user


# ---------------------------
# Post ViewSet
# ---------------------------
class PostViewSet(viewsets.ModelViewSet):
    """CRUD operations for Post."""
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


# ---------------------------
# Comment ViewSet
# ---------------------------
class CommentViewSet(viewsets.ModelViewSet):
    """CRUD operations for Comment."""
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


# ---------------------------
# Feed Pagination
# ---------------------------
class FeedPagination(PageNumberPagination):
    """Pagination settings for feeds."""
    page_size = 10
    page_size_query_param = "page_size"
    max_page_size = 100


# ---------------------------
# Feed List API (Paginated)
# ---------------------------
class FeedListAPIView(generics.ListAPIView):
    """Paginated feed of posts by users the current user follows."""
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = FeedPagination

    def get_queryset(self):
        user = self.request.user
        following_qs = user.following.all()
        if not following_qs.exists():
            return Post.objects.none()
        return Post.objects.filter(author__in=following_qs).order_by("-created_at")


# ---------------------------
# Feed API (Non-paginated)
# ---------------------------
class FeedView(APIView):
    """Non-paginated feed of posts by users the current user follows."""
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        user = request.user
        following_users = user.following.all()
        posts = Post.objects.filter(author__in=following_users).order_by("-created_at")
        serializer = PostSerializer(posts, many=True, context={"request": request})
        return Response(serializer.data)


# ---------------------------
# Like a Post (Function-based)
# ---------------------------
@api_view(["POST"])
@permission_classes([permissions.IsAuthenticated])
def like_post(request, pk):
    """Like a post. Creates a Like and Notification for the post author."""
    post = generics.get_object_or_404(Post, pk=pk)
    user = request.user
    like, created = Like.objects.get_or_create(post=post, user=user)

    if not created:
        return Response({"detail": "Already liked."}, status=status.HTTP_400_BAD_REQUEST)

    if post.author != user:
        Notification.objects.create(
            recipient=post.author,
            actor=user,
            verb="liked your post",
            target_content_type=ContentType.objects.get_for_model(post),
            target_object_id=post.id,
        )

    serializer = LikeSerializer(like, context={"request": request})
    return Response(serializer.data, status=status.HTTP_201_CREATED)


# ---------------------------
# Unlike a Post (Function-based)
# ---------------------------
@api_view(["POST"])
@permission_classes([permissions.IsAuthenticated])
def unlike_post(request, pk):
    """Unlike a post and mark related notifications as read."""
    post = generics.get_object_or_404(Post, pk=pk)
    user = request.user
    deleted, _ = Like.objects.filter(post=post, user=user).delete()

    if deleted:
        Notification.objects.filter(
            recipient=post.author,
            actor=user,
            verb="liked your post",
            target_content_type=ContentType.objects.get_for_model(post),
            target_object_id=post.id,
        ).update(unread=False)
        return Response({"detail": "Unliked."}, status=status.HTTP_200_OK)

    return Response({"detail": "You haven't liked this post."}, status=status.HTTP_400_BAD_REQUEST)


# ---------------------------
# Like a Post (Class-based)
# ---------------------------
class LikePostView(APIView):
    """Alternative APIView version for liking a post."""
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, pk):
        post = generics.get_object_or_404(Post, pk=pk)
        like, created = Like.objects.get_or_create(user=request.user, post=post)
        if created:
            Notification.objects.create(
                recipient=post.author,
                actor=request.user,
                verb="liked your post",
                target_content_type=ContentType.objects.get_for_model(post),
                target_object_id=post.id,
            )
            return Response({'message': 'Post liked successfully.'}, status=status.HTTP_201_CREATED)
        return Response({'message': 'You already liked this post.'}, status=status.HTTP_200_OK)


# ---------------------------
# Unlike a Post (Class-based)
# ---------------------------
class UnlikePostView(APIView):
    """Alternative APIView version for unliking a post."""
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, pk):
        post = generics.get_object_or_404(Post, pk=pk)
        like = Like.objects.filter(user=request.user, post=post).first()
        if like:
            like.delete()
            return Response({'message': 'Post unliked successfully.'}, status=status.HTTP_204_NO_CONTENT)
        return Response({'message': 'You have not liked this post.'}, status=status.HTTP_400_BAD_REQUEST)
