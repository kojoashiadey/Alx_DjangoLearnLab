# users/views.py

from django.contrib.auth import get_user_model
from django.contrib.contenttypes.models import ContentType
from django.shortcuts import get_object_or_404
from rest_framework import generics, status, permissions
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.decorators import api_view, permission_classes
from notifications.models import Notification

from .serializers import RegisterSerializer, UserSerializer
from .models import CustomUser

User = get_user_model()


# ---------------------------
# Registration View
# ---------------------------
class RegisterAPIView(generics.CreateAPIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = RegisterSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        token, _ = Token.objects.get_or_create(user=user)
        return Response(
            {
                "token": token.key,
                "user": UserSerializer(user, context={"request": request}).data,
            },
            status=status.HTTP_201_CREATED,
        )


# ---------------------------
# Custom Login View
# ---------------------------
class CustomObtainAuthToken(ObtainAuthToken):
    """Return token and serialized user data on login."""

    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        token_key = response.data.get("token")
        token = Token.objects.get(key=token_key)
        user = token.user
        return Response(
            {"token": token.key, "user": UserSerializer(user).data},
            status=status.HTTP_200_OK,
        )


# ---------------------------
# Public User Detail
# ---------------------------
class UserDetailAPIView(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.AllowAny]


# ---------------------------
# Authenticated User Profile
# ---------------------------
class MeAPIView(generics.RetrieveUpdateAPIView):
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user


# ---------------------------
# Follow Toggle (Generic View)
# ---------------------------
class FollowToggleAPIView(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, pk):
        target = get_object_or_404(User, pk=pk)
        user = request.user

        if target == user:
            return Response(
                {"detail": "You cannot follow yourself."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Follow or unfollow logic
        if user in target.followers.all():
            target.followers.remove(user)
            return Response({"detail": "Unfollowed"}, status=status.HTTP_200_OK)
        else:
            target.followers.add(user)
            # Create notification when someone follows
            Notification.objects.create(
                recipient=target,
                actor=user,
                verb="started following you",
                target_content_type=None,
                target_object_id=None,
            )
            return Response({"detail": "Followed"}, status=status.HTTP_200_OK)


# ---------------------------
# Function-based Follow APIs
# ---------------------------
@api_view(["POST"])
@permission_classes([permissions.IsAuthenticated])
def follow_user(request, user_id):
    """Authenticated user (request.user) follows another user."""
    if request.user.id == user_id:
        return Response(
            {"detail": "You cannot follow yourself."},
            status=status.HTTP_400_BAD_REQUEST,
        )

    target = get_object_or_404(CustomUser.objects.all(), id=user_id)
    request.user.following.add(target)

    # Create notification after following
    if target != request.user:
        Notification.objects.create(
            recipient=target,
            actor=request.user,
            verb="started following you",
            target_content_type=None,
            target_object_id=None,
        )

    return Response(
        {"detail": f"You are now following {target.username}."},
        status=status.HTTP_200_OK,
    )


@api_view(["POST"])
@permission_classes([permissions.IsAuthenticated])
def unfollow_user(request, user_id):
    """Authenticated user (request.user) unfollows another user."""
    if request.user.id == user_id:
        return Response(
            {"detail": "You cannot unfollow yourself."},
            status=status.HTTP_400_BAD_REQUEST,
        )

    target = get_object_or_404(CustomUser.objects.all(), id=user_id)
    request.user.following.remove(target)
    return Response(
        {"detail": f"You have unfollowed {target.username}."},
        status=status.HTTP_200_OK,
    )


# ---------------------------
# List Following
# ---------------------------
@api_view(["GET"])
@permission_classes([permissions.IsAuthenticated])
def list_following(request):
    """Return a list of users that the current user is following."""
    following_qs = request.user.following.all()
    data = [{"id": u.id, "username": u.username} for u in following_qs]
    return Response(data, status=status.HTTP_200_OK)


# ---------------------------
# List Followers
# ---------------------------
@api_view(["GET"])
@permission_classes([permissions.IsAuthenticated])
def list_followers(request):
    """Return a list of users that follow the current user."""
    followers_qs = request.user.followers.all()
    data = [{"id": u.id, "username": u.username} for u in followers_qs]
    return Response(data, status=status.HTTP_200_OK)
