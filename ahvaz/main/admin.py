from django.contrib import admin
from . import models

# Register your models here.

admin.site.register(models.Setting)
admin.site.register(models.Context)
