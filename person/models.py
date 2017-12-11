from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MinLengthValidator
from django.conf import settings


class CustomUser(AbstractUser):
    confirm_time = models.DateTimeField(blank=True, null=True)
    token = models.CharField(max_length=32, null=True, blank=True)

    def __init__(self, *args, **kwargs):
        self._meta.get_field('is_active').default = False
        super(CustomUser, self).__init__(*args, **kwargs)


class Person(models.Model):
    first_name = models.CharField(max_length=63)
    last_name = models.CharField(max_length=63)
    email = models.EmailField(max_length=70)
    student_card_number = models.CharField(max_length=10, blank=True, null=True, validators=[MinLengthValidator(10)])
    user_id = models.ForeignKey(settings.AUTH_USER_MODEL, blank=True, null=True, on_delete=models.SET_NULL)

    def __str__(self):
        return f'{self.first_name} {self.last_name} ({self.email})'
