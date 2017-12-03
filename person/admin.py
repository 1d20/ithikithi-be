from django.contrib import admin

from person import models


admin.site.register(models.Person)
admin.site.register(models.CustomUser)
