from django.db import models


class Person(models.Model):
    first_name = models.CharField(max_length=63)
    last_name = models.CharField(max_length=63)
    email = models.EmailField(max_length=70, unique=True)
    # TODO: add student_card_number and user_id

    def __str__(self):
        return f'{self.first_name} {self.last_name} ({self.email})'
