from rest_framework import viewsets, status, permissions as django_permissions
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
        return Response(
            data=Serializer.serialize(stations),
            status=status.HTTP_200_OK,
        )

    @list_route(methods=['get'])
    def trains(self, request):
        request_params = {}
        get_data = request.query_params
        required_fields = ['station_from_id', 'station_to_id', 'date_dep']
        if all([attr in get_data for attr in required_fields]):
            enable_params = required_fields + ['time_dep', 'time_dep_till', 'another_ec', 'search']
            for attr, val in get_data.items():
                if attr in enable_params:
                    request_params[attr] = val
            result = client.trains(**request_params)
            return Response(
                data=Serializer.serialize(result),
                status=status.HTTP_200_OK,
            )
        else:
            return Response(
                data='bad_request',
                status=status.HTTP_400_BAD_REQUEST,
            )
