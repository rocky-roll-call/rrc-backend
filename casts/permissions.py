"""
Custom Cast permissions
"""

from rest_framework import permissions


class IsManager(permissions.BasePermission):
    """
    Permission class to only allow managers to edit a cast object
    """

    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        if hasattr(obj, "cast"):
            return obj.cast.is_manager(request.user.profile)
        return obj.is_manager(request.user.profile)


class IsManagerOrReadOnly(permissions.BasePermission):
    """
    Permission class to only allow managers to edit a cast object or provide read access
    """

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        if hasattr(obj, "cast"):
            return obj.cast.is_manager(request.user.profile)
        return obj.is_manager(request.user.profile)
