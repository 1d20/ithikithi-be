# Generated by Django 2.0 on 2017-12-03 18:21

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('booking', '0003_auto_20171203_1812'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bookingperson',
            name='created_on',
            field=models.DateTimeField(default=datetime.datetime(2017, 12, 3, 18, 21, 7, 816371, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='bookingperson',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2017, 12, 3, 18, 21, 7, 816210, tzinfo=utc)),
        ),
    ]