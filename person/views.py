from rest_framework import viewsets

from person import serializers, models


class PersonViewSet(viewsets.ModelViewSet):
    queryset = models.Person.objects.all()
    serializer_class = serializers.PersonSerializer
