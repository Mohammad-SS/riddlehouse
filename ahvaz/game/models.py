from django.db import models
from django.contrib.postgres import fields as postgres_fields
from persiantools import jdatetime

from riddlehouse.helpers import enums


class Room(models.Model):
    name = models.CharField(max_length=255)
    difficulty = models.CharField(blank=True, null=True, max_length=3)
    min_players = models.IntegerField(blank=True, null=True)
    max_players = models.IntegerField(blank=True, null=True)
    conditions = models.TextField(blank=True, null=True)
    game_duration = models.CharField(max_length=255, blank=True, null=True)
    price_per_unit = models.IntegerField(blank=True, null=True)
    default_hours = postgres_fields.ArrayField(models.CharField(max_length=12, blank=True))
    default_days = postgres_fields.ArrayField(models.IntegerField(choices=enums.WeekDays.choices))
    room_type = models.CharField(max_length=7, choices=enums.RoomType.choices, default=enums.RoomType.REAL)
    box_packages_prices = postgres_fields.ArrayField(models.IntegerField(), blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    warnings = models.TextField(blank=True, null=True)
    banner = models.ImageField(upload_to="rooms", blank=True, null=True)

    def __str__(self):
        return self.name


class Exclusion(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name="exclusions")
    role = models.CharField(max_length=4, choices=enums.ExclusionsType.choices,
                            default=enums.ExclusionsType.DATE_AND_WEEKDAY)
    from_date = models.DateField(blank=True, null=True)
    to_date = models.DateField(blank=True, null=True)
    weekdays = postgres_fields.ArrayField(models.IntegerField(choices=enums.WeekDays.choices, blank=True, null=True),
                                          blank=True, null=True)
    hours = postgres_fields.ArrayField(models.CharField(max_length=12, blank=True), blank=True, null=True)
    create_date = models.DateTimeField(auto_now_add=True, blank=True, null=True)

    def __str__(self):
        return f"{self.room.name} - ({self.from_date} - {self.to_date})"

    @property
    def persian_dates(self):
        from_date = jdatetime.JalaliDate(self.from_date).replace(locale="fa").strftime(
            "%Y/%m/%d %A")
        to_date = jdatetime.JalaliDate(self.to_date).replace(locale="fa").strftime(
            "%Y/%m/%d %A")
        created_date = jdatetime.JalaliDate(self.create_date).replace(locale="fa").strftime(
            "%Y/%m/%d %A")

        return {
            "from": from_date,
            "created": created_date,
            "to": to_date
        }
