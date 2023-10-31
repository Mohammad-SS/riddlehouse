import pytz
from django.db import models
from django.contrib.postgres import fields as postgres_fields
from django.urls import reverse
from persiantools import jdatetime
from riddlehouse.helpers import functions
from django.template.defaultfilters import slugify
from riddlehouse.helpers import enums
from unidecode import unidecode
from django.utils.timezone import datetime
import calendar

class Room(models.Model):
    name = models.CharField(max_length=255)
    difficulty = models.CharField(blank=True, null=True, max_length=3)
    slug = models.CharField(max_length=63, default="", blank=True, null=True)
    min_players = models.IntegerField(blank=True, null=True)
    max_players = models.IntegerField(blank=True, null=True)
    conditions = models.TextField(blank=True, null=True)
    game_duration = models.CharField(max_length=255, blank=True, null=True)
    price_per_unit = models.IntegerField(blank=True, null=True)
    pre_pay = models.IntegerField(blank=True, null=True)
    default_hours = postgres_fields.ArrayField(models.CharField(max_length=12, blank=True))
    default_days = postgres_fields.ArrayField(models.IntegerField(blank=True))
    room_type = models.CharField(max_length=7, choices=enums.RoomType.choices, default=enums.RoomType.REAL)
    box_packages_prices = postgres_fields.ArrayField(models.IntegerField(), blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    warnings = models.TextField(blank=True, null=True)
    banner = models.ImageField(upload_to="rooms", blank=True, null=True)
    modified_time = models.DateTimeField(auto_now=True)
    admin_phones = models.CharField(default="", max_length=127, blank=True, null=True)
    google_map = models.TextField(blank=True, null=True)
    balad_link = models.TextField(blank=True, null=True)
    is_archive = models.BooleanField(default=False)
    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.id:
            self.slug = functions.slugify(self.name)

        super(Room, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("main:room-page", args=[self.slug])


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


class OneTimeExclusion(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name="otes")
    date_time = models.DateTimeField(blank=True, null=True)
    closed = models.BooleanField(blank=True, null=True)
    create_date = models.DateTimeField(auto_now_add=True, blank=True, null=True)

    def __str__(self):
        return f"{self.room.name} - ({self.date_time})"

    @property
    def persian_dates(self):
        jdatetime.JalaliDateTime.fromtimestamp(self.date_time.timestamp()).replace(
            locale="fa").strftime(
            "%Y/%m/%d %A %H:%M")
        date = {
            "value": jdatetime.JalaliDateTime.fromtimestamp(self.date_time.timestamp()).replace(locale="en").strftime("%Y/%m/%d"),
            "display": jdatetime.JalaliDateTime.fromtimestamp(self.date_time.timestamp()).replace(locale="fa").strftime("%A %d %B %Y")
        }
        time = jdatetime.JalaliDateTime.fromtimestamp(self.date_time.timestamp()).replace(locale="en").strftime("%H:%M")
        created_date = jdatetime.JalaliDateTime(self.create_date, locale='en',tzinfo=pytz.timezone("Asia/Tehran")).strftime(
            "%Y/%m/%d %A")

        print('-' * 50)
        print(date, time)
        print('-' * 50)
        return {
            "date": date,
            "time": time,
            "created": created_date,
        }


# Function to generate choices for days in the current month
def get_current_month_day_choices():
    now = datetime.now()
    _, last_day = calendar.monthrange(now.year, now.month)
    choices = [(str(day), str(day)) for day in range(1, last_day + 1)]
    return choices


class VipSans(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name='vipsans')
    price_per_unit = models.IntegerField(blank=True, null=True)
    pre_pay = models.IntegerField(blank=True, null=True)
    from_date = models.DateField(blank=True, null=True)
    to_date = models.DateField(blank=True, null=True)
    weekdays = postgres_fields.ArrayField(models.IntegerField(choices=enums.WeekDays.choices, blank=True, null=True),
                                          blank=True, null=True)
    
    hours = postgres_fields.ArrayField(models.CharField(max_length=12, blank=True), blank=True, null=True)
    create_date = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    test = models.CharField(max_length=50, blank=True, null=True)

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
    
    def __str__(self):
        return f"{self.room.name} - ({self.from_date} - {self.to_date})"

class OneTimeVipSans(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    date_time = models.DateTimeField(blank=True, null=True)
    price_per_unit = models.IntegerField(blank=True, null=True)
    pre_pay = models.IntegerField(blank=True, null=True)
    exclude = models.IntegerField(default=False, blank=True, null=True)
    
    def __str__(self):
        return f"{self.room.name} - ({self.date_time})"

    @property
    def persian_dates(self):
        jdatetime.JalaliDateTime.fromtimestamp(self.date_time.timestamp()).replace(
            locale="fa").strftime(
            "%Y/%m/%d %A %H:%M")
        date = {
            "value": jdatetime.JalaliDateTime.fromtimestamp(self.date_time.timestamp()).replace(locale="en").strftime("%Y/%m/%d"),
            "display": jdatetime.JalaliDateTime.fromtimestamp(self.date_time.timestamp()).replace(locale="fa").strftime("%A %d %B %Y")
        }
        time = jdatetime.JalaliDateTime.fromtimestamp(self.date_time.timestamp()).replace(locale="en").strftime("%H:%M")
        created_date = jdatetime.JalaliDateTime(self.create_date, locale='en',tzinfo=pytz.timezone("Asia/Tehran")).strftime(
            "%Y/%m/%d %A")

        print('-' * 50)
        print(date, time)
        print('-' * 50)
        return {
            "date": date,
            "time": time,
            "created": created_date,
        }