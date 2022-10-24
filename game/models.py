from django.db import models
from django.contrib.postgres import fields as postgres_fields
from riddlehouse.helpers import enums


class Room(models.Model):
    name = models.CharField(max_length=255)
    difficulty = models.IntegerField(blank=True,null=True)
    min_players = models.IntegerField(blank=True,null=True)
    max_players = models.IntegerField(blank=True,null=True)
    conditions = models.TextField(blank=True,null=True)
    game_duration = models.CharField(max_length=255 , blank=True,null=True)
    price_per_unit = models.IntegerField(blank=True,null=True)
    default_hours = postgres_fields.ArrayField(models.CharField(max_length=12, blank=True))
    default_days = postgres_fields.ArrayField(models.IntegerField(choices=enums.WeekDays.choices))
    room_type = models.CharField(max_length=7 , choices=enums.RoomType.choices , default=enums.RoomType.REAL)
    box_packages_prices = postgres_fields.ArrayField(models.IntegerField() , blank=True,null=True)
    description = models.TextField(blank=True,null=True)
    warnings = models.TextField(blank=True,null=True)
    banner = models.ImageField(upload_to="rooms" , blank=True,null=True)

class Exclusion(models.Model):
    room = models.ForeignKey(Room,on_delete=models.CASCADE , related_name="exclusions")
    zone = postgres_fields.DateTimeRangeField(name="zones")
    is_suspended = models.BooleanField(default=True)


