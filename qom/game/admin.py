from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Room , Exclusion , OneTimeExclusion, VipSans, OneTimeVipSans


admin.site.register((Room, Exclusion, OneTimeExclusion, VipSans, OneTimeVipSans))