import secrets

from rest_framework import viewsets, status

from django.utils import timezone
from datetime import timedelta

from django.contrib.auth import authenticate, login, logout
from rest_framework.decorators import list_route, detail_route
from rest_framework.response import Response
from django.core.mail import send_mail
from ithikithi.settings import EMAIL_HOST_USER
from person import serializers, models


class PersonViewSet(viewsets.ModelViewSet):
    queryset = models.Person.objects.all()
    serializer_class = serializers.PersonSerializer


class AuthenticationViewSet(viewsets.ViewSet):
    serializer_class = serializers.AuthenticationSerializer

    @list_route(methods=['post'])
    def login(self, request):
        data = request.data
        serializer = self.serializer_class(data=data)
        if serializer.is_valid():
            user = authenticate(username=data['email'], password=data['password'])
            if user and user.customuser.is_confirmed:
                login(request, user)
                return Response(
                    data=serializers.CustomUserSerializer(user.customuser).data,
                    status=status.HTTP_200_OK,
                )
        return Response(
            data=serializer.errors,
            status=status.HTTP_400_BAD_REQUEST,
        )

    @list_route(methods=['post'])
    def signup(self, request):
        data = request.data
        serializer = self.serializer_class(data=data)
        if serializer.is_valid():
            user = models.CustomUser.objects.filter(email=data['email'])
            if not user:
                user = models.CustomUser.objects.create_user(
                    username=data['email'],
                    email=data['email'],
                    password=data['password'],
                )
                token = secrets.token_urlsafe(20)
                send_mail(
                    subject='Test',
                    message='''Test %s ''' % (request.META['HTTP_ORIGIN'] + '/api/person/authenticate/confirm/' + token),
                    from_email=EMAIL_HOST_USER,
                    recipient_list=[data['email']],
                    fail_silently=False
                )
                user.token = token
                user.confirm_time = timezone.now()
                user.save()
                return Response({
                    'data': serializers.CustomUserSerializer(user).data,
                    'status': status.HTTP_201_CREATED,
                })
            else:
                return Response({
                    'data': 'user_already_exists',
                    'status': status.HTTP_400_BAD_REQUEST,
                })
        else:
            return Response({
                'data': 'validation_error',
                'status': status.HTTP_400_BAD_REQUEST,
            })

    @list_route(methods=['get'])
    def logout(self, request):
        user = request.user
        if user.is_authenticated:
            logout(request)
            return Response({
                'data': 'OK',
                'status': status.HTTP_200_OK,
            })
        return Response({
            'data': 'guest user',
            'status': status.HTTP_400_BAD_REQUEST,
        })

    @list_route(methods=['get'], url_path='confirm/(?P<token>[a-zA-Z0-9_-]+)')
    def confirm(self, request, token):
        current_datetime = timezone.now()
        days_link_enable = 1
        user = models.CustomUser.objects.filter(
            token=token,
            is_confirmed=False,
            confirm_time__range=((current_datetime - timedelta(days=days_link_enable)), current_datetime)
        )
        if user and len(user) == 1:
            user[0].is_confirmed = True
            user[0].save()
            return Response({
                'data': 'OK',
                'status': status.HTTP_200_OK,
            })
        return Response({
            'data': 'FAIL',
            'status': status.HTTP_400_BAD_REQUEST,
        })