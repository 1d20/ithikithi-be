from rest_framework import viewsets, permissions as django_permissions
from rest_framework.decorators import list_route
from rest_framework.response import Response
from uz_api import ClientInteface, Serializer

from booking import serializers, models, permissions


client = ClientInteface()


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


class UZViewSet(viewsets.ViewSet):

    @list_route(methods=['get'])
    def stations(self, request):
        stations = client.stations(name=request.query_params.get('name', ''))
        return Response(data=Serializer.serialize(stations))
