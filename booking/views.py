from rest_framework import viewsets, permissions as django_permissions

from booking import serializers, models, permissions


class BookingViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.BookingSerializer
    permission_classes = (permissions.BookingPermission, django_permissions.IsAuthenticated,)

    def get_queryset(self):
        return models.Booking.objects.filter(user_id=self.request.user)


class BookingPersonViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.BookingPersonSerializer
    permission_classes = (django_permissions.IsAuthenticated, permissions.IsBookingPersonPermissions)

    def get_queryset(self):
        return models.BookingPerson.objects.filter(booking_id__user_id=self.request.user)
