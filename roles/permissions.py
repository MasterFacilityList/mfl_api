from rest_framework import permissions
from django.contrib.auth.models import AnonymousUser


class MFLPermission(permissions.BasePermission):
    def has_permission(self, request, view):

        if request.method in permissions.SAFE_METHODS:
            return True
        else:
            # ensures that methods for patches and posts and
            # deletes are only accessed by authenticated users
            if isinstance(request.user, AnonymousUser):
                return False
            else:
                return True
