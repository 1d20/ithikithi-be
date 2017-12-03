from rest_framework import serializers

from booking import models


class BookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Booking
        fields = '__all__'


class BookingPersonSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.BookingPerson
        fields = '__all__'