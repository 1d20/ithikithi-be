from django.db import models
from django.utils import timezone
from django.conf import settings


class Booking(models.Model):
    user_id = models.ForeignKey(settings.AUTH_USER_MODEL, blank=True, null=True, on_delete=models.SET_NULL)
    email = models.EmailField()

    def __str__(self):
        return f'{self.email}'


class BookingPerson(models.Model):
    booking_id = models.ForeignKey(Booking, on_delete=models.CASCADE)
    from_location = models.CharField(max_length=1000) # TODO change to JsonField for PostgreSQL
    to_location = models.CharField(max_length=1000) # TODO change to JsonField for PostgreSQL
    date = models.DateTimeField(default=timezone.now)
    train_number = models.CharField(max_length=8)
    wagon = models.CharField(max_length=5)
    place = models.CharField(max_length=5)
    first_name = models.CharField(max_length=63)
    last_name = models.CharField(max_length=63)
    email = models.EmailField()
    student_card_number = models.CharField(max_length=10)
    created_on = models.DateTimeField(default=timezone.now)
    need_to_change_ticket = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.email} {self.train_number} {self.wagon} {self.place}'
