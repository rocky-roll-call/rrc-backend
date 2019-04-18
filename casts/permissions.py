"""
Custom Cast permissions
"""

from rest_framework import permissions


def check_manager(obj, profile) -> bool:
    """
    Returns True if the user is a manager of the object or its parent Cast
    """
    # This first level is for getting objects to a potential cast relation
    for key in ("event",):
        if hasattr(obj, key):
            obj = getattr(obj, key)
            break
    if hasattr(obj, "cast"):
        obj = obj.cast
    return obj.is_manager(profile)


class IsManager(permissions.BasePermission):
    """
    Permission class to only allow managers to edit a cast object
    """

    def has_permission(self, request, view) -> bool:
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj) -> bool:
        return check_manager(obj, request.user.profile)


class IsManagerOrReadOnly(permissions.BasePermission):
    """
    Permission class to only allow managers to edit a cast object or provide read access
    """

    def has_object_permission(self, request, view, obj) -> bool:
        if request.method in permissions.SAFE_METHODS:
            return True
        return check_manager(obj, request.user.profile)
