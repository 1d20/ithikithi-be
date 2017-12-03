from rest_framework.permissions import BasePermission


class BookingPermission(BasePermission):

    def has_object_permission(self, request, view, obj):
        return request.user.id == obj.user_id.id or request.user.is_staff


class IsBookingPersonPermissions(BasePermission):

    def has_object_permission(self, request, view, obj):
        return request.user.id == obj.booking_id.user_id.id