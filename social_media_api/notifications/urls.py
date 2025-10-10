# notifications/urls.py
from django.urls import path
from .views import NotificationListAPIView, MarkNotificationReadAPIView, MarkAllReadAPIView

urlpatterns = [
    path("", NotificationListAPIView.as_view(), name="notifications-list"),
    path("<int:pk>/read/", MarkNotificationReadAPIView.as_view(), name="notification-read"),
    path("mark-all-read/", MarkAllReadAPIView.as_view(), name="notifications-mark-all-read"),
]
