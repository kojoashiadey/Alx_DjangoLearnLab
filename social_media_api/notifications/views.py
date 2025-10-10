# notifications/views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated


class NotificationListAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response({"message": "Notification list placeholder"})


class MarkNotificationReadAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        return Response({"message": f"Marked notification {pk} as read"})


class MarkAllReadAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        return Response({"message": "All notifications marked as read"})
