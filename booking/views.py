from rest_framework import viewsets

from booking import serializers, models


class BookingViewSet(viewsets.ModelViewSet):
    queryset = models.Booking.objects.all()
    serializer_class = serializers.BookingSerializer


class BookingPersonViewSet(viewsets.ModelViewSet):
    queryset = models.BookingPerson.objects.all()
    serializer_class = serializers.BookingPersonSerializer
