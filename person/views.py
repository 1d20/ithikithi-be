import secrets

from rest_framework import viewsets, status, exceptions

from django.utils import timezone
from datetime import timedelta

from django.contrib.auth import authenticate, login, logout
from rest_framework.decorators import list_route, permission_classes
from rest_framework.response import Response
from django.core.mail import send_mail
from ithikithi.settings import EMAIL_HOST_USER
from person import serializers, models, permissions
from rest_framework import permissions as django_permissions


class PersonViewSet(viewsets.ModelViewSet):
    queryset = models.Person.objects.all()
    serializer_class = serializers.PersonSerializer
    permission_classes = (django_permissions.IsAuthenticated,)

    def create(self, request, *args, **kwargs):
        data = request.data
        serializer = self.serializer_class(data=data)
        if not serializer.is_valid():
            raise exceptions.ValidationError()

        email_exist = models.Person.objects.filter(user_id=request.user, email=data.get('email')).exists()
        if email_exist:
            raise exceptions.ParseError(detail='already_added')

        person = models.Person()
        for attr in ['first_name', 'last_name', 'email', 'student_card_number']:
            setattr(person, attr, data.get(attr))

        person.user_id = models.CustomUser.objects.get(user_ptr_id=request.user.id)
        person.save()
        return Response(
            data=serializers.PersonSerializer(person).data,
            status=status.HTTP_201_CREATED,
        )

    @list_route(methods=['get'])
    def get_queryset(self):
        return models.Person.objects.filter(user_id=self.request.user)


class AuthenticationViewSet(viewsets.ViewSet):
    serializer_class = serializers.AuthenticationSerializer

    @list_route(methods=['post'])
    @permission_classes(permissions.IsNotAuthenticated)
    def login(self, request):
        data = request.data
        serializer = self.serializer_class(data=data)
        if serializer.is_valid():
            user = authenticate(username=data['email'], password=data['password'])
            if user and user.is_active:
                login(request, user)
                return Response(
                    data=serializers.CustomUserSerializer(user).data,
                    status=status.HTTP_200_OK,
                )
        raise exceptions.ValidationError()

    @list_route(methods=['post'])
    @permission_classes(permissions.IsNotAuthenticated)
    def signup(self, request):
        data = request.data
        serializer = self.serializer_class(data=data)
        if not serializer.is_valid():
            raise exceptions.ValidationError()

        user = models.CustomUser.objects.filter(email=data['email'])
        if user:
            raise exceptions.ParseError(detail='user_already_exists')

        user = models.CustomUser.objects.create_user(
            username=data['email'],
            email=data['email'],
            password=data['password'],
        )
        token = secrets.token_urlsafe(20)
        send_mail(
            subject='Test',
            message='''Test %s ''' % (request.build_absolute_uri('/') + 'api/person/authenticate/confirm/' + token),
            from_email=EMAIL_HOST_USER,
            recipient_list=[data['email']],
            fail_silently=False
        )
        user.token = token
        user.confirm_time = timezone.now()
        user.save()
        return Response(
            data=serializers.CustomUserSerializer(user).data,
            status=status.HTTP_201_CREATED,
        )

    @list_route(methods=['get'])
    @permission_classes(django_permissions.IsAuthenticated)
    def logout(self, request):
        user = request.user
        if user.is_authenticated:
            return Response(
                data='guest user',
                status=status.HTTP_400_BAD_REQUEST,
            )

        logout(request)
        return Response(
            data='OK',
            status=status.HTTP_200_OK,
        )

    @list_route(methods=['get'], url_path='confirm/(?P<token>[a-zA-Z0-9_-]+)')
    @permission_classes(django_permissions.AllowAny)
    def confirm(self, request, token):
        current_datetime = timezone.now()
        days_link_enable = 1
        user = models.CustomUser.objects.filter(
            token=token,
            is_confirmed=False,
            confirm_time__range=((current_datetime - timedelta(days=days_link_enable)), current_datetime)
        )
        if not (user and len(user) == 1):
            raise exceptions.ParseError(detail='FAIL')

        user[0].is_active = True
        user[0].save()
        return Response(
            data='OK',
            status=status.HTTP_200_OK,
        )
