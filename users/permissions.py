"""
Custom object permissions
"""

from rest_framework import permissions


class IsUser(permissions.BasePermission):
    """
    Permission class to only allow users to edit their own User object
    """

    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        return obj == request.user


class IsOwner(IsUser):
    """
    Permission class to only allow owners to edit an object
    """

    def has_object_permission(self, request, view, obj):
        if hasattr(obj, "profile"):
            return obj.profile.user == request.user
        return obj.user == request.user


class IsOwnerOrReadOnly(IsUser):
    """
    Permission class to only allow owners to edit an object or provide read access
    """

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        if hasattr(obj, "profile"):
            return obj.profile.user == request.user
        return obj.user == request.user
