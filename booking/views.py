from rest_framework import viewsets
from rest_framework.decorators import list_route
from rest_framework.response import Response
from uz_api import ClientInteface, Serializer

from booking import serializers, models


client = ClientInteface()


class BookingViewSet(viewsets.ModelViewSet):
    queryset = models.Booking.objects.all()
    serializer_class = serializers.BookingSerializer


class BookingPersonViewSet(viewsets.ModelViewSet):
    queryset = models.BookingPerson.objects.all()
    serializer_class = serializers.BookingPersonSerializer


class UZViewSet(viewsets.ViewSet):

    @list_route(methods=['get'])
    def stations(self, request):
        stations = client.stations(name=request.query_params.get('name', ''))
        return Response(data=Serializer.serialize(stations))
