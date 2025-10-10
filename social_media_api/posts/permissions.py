# posts/permissions.py
from rest_framework import permissions

class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Custom permission: only owners can edit or delete objects.
    Read-only methods are allowed for everyone.
    """

    def has_object_permission(self, request, view, obj):
        # Read-only -> allow
        if request.method in permissions.SAFE_METHODS:
            return True
        # Write -> only the object's author can edit/delete
        return getattr(obj, "author", None) == request.user
