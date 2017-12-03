from rest_framework.permissions import BasePermission


class IsNotAuthenticated(BasePermission):

    def has_permission(self, request, view):
        return not request.user


class IsPersonOwner(BasePermission):

    def has_object_permission(self, request, view, obj):
        return request.user.id == obj.user_id.id
