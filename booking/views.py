from rest_framework import viewsets, status, permissions as django_permissions
from rest_framework.decorators import list_route
from rest_framework.response import Response
from uz_api import ClientInteface, Serializer

from booking import serializers, models, permissions, fields


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
        if fields.validate(request.query_params, 'stations'):
            stations = client.stations(name=request.query_params.get('name', ''))
            return Response(
                data=Serializer.serialize(stations),
                status=status.HTTP_200_OK,
            )
        else:
            return Response(
                data='invalid_data',
                status=status.HTTP_400_BAD_REQUEST,
            )

    @list_route(methods=['get'])
    def trains(self, request):
        data = request.query_params
        if fields.validate(data, 'trains'):
            request_params = fields.prepare_params(data, 'trains')
            result = client.trains(**request_params)
            return Response(
                data=Serializer.serialize(result),
                status=status.HTTP_200_OK,
            )
        else:
            return Response(
                data='invalid_data',
                status=status.HTTP_400_BAD_REQUEST,
            )

    @list_route(methods=['get'])
    def coaches(self, request):
        data = request.query_params
        if fields.validate(data, 'coaches'):
            request_params = fields.prepare_params(data, 'coaches')
            result = client.coaches(**request_params)
            return Response(
                data=Serializer.serialize(result),
                status=status.HTTP_200_OK,
            )
        else:
            return Response(
                data='invalid_data',
                status=status.HTTP_400_BAD_REQUEST,
            )