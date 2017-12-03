from rest_framework import viewsets, status

from person import serializers, models
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from rest_framework.decorators import list_route
from rest_framework.response import Response


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
            if user:
                login(request, user)
                return Response(
                    data=serializers.UserSerializer(user).data,
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
            user = User.objects.filter(email=data['email'])
            if not user:
                user = User.objects.create_user(
                    username=data['email'],
                    email=data['email'],
                    password=data['password'],
                )
                return Response({
                    'data': serializers.UserSerializer(user).data,
                    'status': status.HTTP_201_CREATED,
                })
            else:
                return Response({
                    'data': 'user already exists',
                    'status': status.HTTP_400_BAD_REQUEST,
                })
        else:
            return Response({
                'data': 'validation error',
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
