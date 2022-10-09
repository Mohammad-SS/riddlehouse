from django.db import models
from enum import Enum


class WeekDays(models.IntegerChoices):
    SATURDAY = 1, "شنبه"
    SUNDAY = 2, "یک شنبه"
    MONDAY = 3, "دو شنبه"
    TUESDAY = 4, "سه شنبه"
    WENDSAY = 5, "چهار شنبه"
    THURSDAY = 6, "پنج شنبه"
    FRIDAY = 7, "جمعه"


class RoomPaymentMethod(models.TextChoices):
    PER_PERSON = "P", "Per Person"
    TOTAL = "T", "Total"


class CouponsType(models.TextChoices):
    PERCENTAGE = "P", "%"
    CONSTANT = "C", "Const"


class RuleTypes(models.TextChoices):
    SINGLE_DAY = "D", "Single Day"
    WEEK_DAY = "W", "Week Day"


class DefaultSettings(Enum):
    LIMIT_DAYS_FOR_RESERVATION = {"slug": "limits_day_reservation", "default": 30}
