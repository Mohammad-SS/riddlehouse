from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Room , Exclusion


admin.site.register(Room)
admin.site.register(Exclusion)