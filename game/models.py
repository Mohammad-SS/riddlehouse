from django.db import models
from django.contrib.postgres import fields as postgres_fields
from riddlehouse.helpers import enums


class Room(models.Model):
    name = models.CharField(max_length=255)
    difficulty = models.IntegerField()
    min_players = models.IntegerField()
    max_players = models.IntegerField()
    game_duration = models.CharField(max_length=255)
    pre_payment = models.IntegerField()
    final_payment = models.IntegerField()
    default_hours = postgres_fields.ArrayField(models.CharField(max_length=12, blank=True))
    default_days = postgres_fields.ArrayField(models.IntegerField(choices=enums.WeekDays.choices))
    final_payment_method = models.CharField(max_length=1, choices=enums.RoomPaymentMethod.choices,
                                            default=enums.RoomPaymentMethod.PER_PERSON)
    description = models.TextField()
    warnings = models.TextField()


class Rule(models.Model):
    name = models.CharField(max_length=255)
    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name="rules")
    date = models.DateField(null=True, blank=True)
    rule_by = models.CharField(max_length=1, choices=enums.RuleTypes.choices, default=enums.RuleTypes.SINGLE_DAY)
    week_day = models.IntegerField(choices=enums.WeekDays.choices, blank=True, null=True)


class Exclusion(models.Model):
    room = models.ForeignKey(Room,on_delete=models.CASCADE , related_name="exclusions")
    zone = postgres_fields.DateTimeRangeField(name="zones")
    is_suspended = models.BooleanField(default=True)