# notifications/serializers.py
from rest_framework import serializers
from .models import Notification
from django.contrib.contenttypes.models import ContentType

class NotificationSerializer(serializers.ModelSerializer):
    actor = serializers.StringRelatedField()
    target_repr = serializers.SerializerMethodField()

    class Meta:
        model = Notification
        fields = ("id", "actor", "verb", "target_repr", "unread", "timestamp")

    def get_target_repr(self, obj):
        if obj.target is None:
            return None
        return str(obj.target)
