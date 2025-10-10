# posts/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    PostViewSet,
    CommentViewSet,
    FeedView,
    FeedListAPIView,
    like_post,
    unlike_post,
    LikePostView,
    UnlikePostView,
)

router = DefaultRouter()
router.register(r"posts", PostViewSet, basename="post")
router.register(r"comments", CommentViewSet, basename="comment")

urlpatterns = [
    # CRUD endpoints
    path("", include(router.urls)),

    # Feed endpoints (both paginated and unpaginated)
    path("feed/", FeedView.as_view(), name="feed"),
    path("feed/paginated/", FeedListAPIView.as_view(), name="feed-paginated"),

    # Like and Unlike (function-based)
    path("posts/<int:pk>/like/", like_post, name="post-like"),
    path("posts/<int:pk>/unlike/", unlike_post, name="post-unlike"),

    # Like and Unlike (class-based)
    path("posts/<int:pk>/like-view/", LikePostView.as_view(), name="like-post-view"),
    path("posts/<int:pk>/unlike-view/", UnlikePostView.as_view(), name="unlike-post-view"),
]
