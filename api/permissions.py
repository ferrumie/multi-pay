from rest_framework import permissions


class IsOwner(permissions.BasePermission):
    """
    Object-level permission to only allow owners to have access to the requests
    """

    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request,
        # Instance must have an attribute named `owner`.
        return obj.user == request.user
