from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Room, Rule , Exclusion


class RuleInline(admin.TabularInline):
    model = Rule


class Rules(admin.ModelAdmin):
    inlines = [
        RuleInline
    ]



admin.site.register(Room, Rules)
admin.site.register(Exclusion)