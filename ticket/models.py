from django.db import models
from django.contrib.auth.models import User
from booking.models import BookingPerson


class Ticket(models.Model):
    user = models.ManyToManyField(User)
    booking_person_id = models.OneToOneField(BookingPerson, on_delete=models.DO_NOTHING)

    def __str__(self):
        return f'{self.booking_person_id.from_location} {self.booking_person_id.to_location} ' \
               f'{self.booking_person_id.date} {self.booking_person_id.train_number}'