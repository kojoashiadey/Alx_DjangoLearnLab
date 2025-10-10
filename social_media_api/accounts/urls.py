# accounts/urls.py
from django.urls import path
from .views import RegisterAPIView, CustomObtainAuthToken, UserDetailAPIView, MeAPIView, FollowToggleAPIView
from .views import follow_user, unfollow_user, list_following, list_followers

urlpatterns = [
    path("register/", RegisterAPIView.as_view(), name="register"),
    path("login/", CustomObtainAuthToken.as_view(), name="login"),
    path("profile/<int:pk>/", UserDetailAPIView.as_view(), name="user-detail"),
    path("me/", MeAPIView.as_view(), name="me"),
    path("follow/<int:pk>/", FollowToggleAPIView.as_view(), name="follow-toggle"),
]

urlpatterns += [
    path("follow/<int:user_id>/", follow_user, name="follow-user"),
    path("unfollow/<int:user_id>/", unfollow_user, name="unfollow-user"),
    path("following/", list_following, name="list-following"),
    path("followers/", list_followers, name="list-followers"),
]
