from django.db import models
from django.contrib.auth.models import User as DjangoUser
from django.core.validators import MinLengthValidator


class CustomUser(DjangoUser):
    is_confirmed = models.BooleanField(default=False)
    confirm_time = models.DateTimeField(blank=True, null=True)
    token = models.CharField(max_length=32, null=True, blank=True)


class Person(models.Model):
    first_name = models.CharField(max_length=63)
    last_name = models.CharField(max_length=63)
    email = models.EmailField(max_length=70)
    student_card_number = models.CharField(max_length=10, blank=True, null=True, validators=[MinLengthValidator(10)])
    user_id = models.ForeignKey(CustomUser, blank=True, null=True, on_delete=models.SET_NULL)

    def __str__(self):
        return f'{self.first_name} {self.last_name} ({self.email})'
