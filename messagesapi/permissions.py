from rest_framework import permissions


class IsOwnerOrCantDelete(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):

        if request.method != "DELETE":
            return True

        return obj.sender == request.user or obj.receiver == request.user
