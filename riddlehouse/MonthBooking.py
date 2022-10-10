import datetime
import random

from django.core.exceptions import ObjectDoesNotExist
from persiantools.jdatetime import JalaliDate, JalaliDateTime

from game import models
from riddlehouse.helpers import enums
from riddlehouse.helpers import functions


class Month():
    month_range = 30

    def __init__(self, month, year=None):
        self.month = month
        if not year:
            self.year = JalaliDate.today().year
        else:
            self.year = year

        self.month_range = JalaliDate.days_in_month(self.month, self.year)
        self.first_day_weekday = JalaliDate(self.year, self.month, 1).isoweekday()

    def create_calander(self, room_id=None):
        calendar = dict()
        week_num = 0
        calendar[0] = dict()
        try:
            room = models.Room.objects.get(pk=room_id)
        except ObjectDoesNotExist as e:
            print(e)
            return None
        for day in range(1, self.month_range + 1):
            this_day = dict()
            this_weekday = JalaliDate(self.year, self.month, day).isoweekday()

            if this_weekday == 1 and not day == 1:
                week_num += 1
                calendar[week_num] = dict()
            this_day['date'] = "{}/{}/{}".format(self.year, self.month, day)
            this_day["weekday"] = this_weekday
            this_day["selectable"] = self.is_day_selectable(day)
            this_day['times'] = self.get_this_day_times(day, room)
            calendar[week_num][day] = this_day
        return calendar

    def get_this_day_times(self, day, room):
        hours = dict()
        this_day = JalaliDate(self.year, self.month, day, locale="fa")
        if not this_day.isoweekday() in room.default_days:
            return hours
        for hour in room.default_hours:
            this_hour, this_minutes = hour.split(":")
            this_timestamp = JalaliDateTime(self.year, self.month, day, int(this_hour),
                                            int(this_minutes)).timestamp()
            hours[hour] = dict()
            hours[hour]["timestamp"] = this_timestamp
            hours[hour]['is_reservable'], hours[hour]['status'] = self.check_hour(this_timestamp, room)
            hours[hour]['rand_id'] = "_{}".format(random.randint(10000, 99999))
        return hours

    @classmethod
    def check_hour(cls, timestamp, room: models.Room):
        # check ORDERS DATABASE
        this_hour = datetime.datetime.fromtimestamp(timestamp)
        is_excluded = room.exclusions.filter(zones__contains=this_hour).exists()
        if is_excluded:
            return False, "CLOSED"

        is_ordered = room.orders.filter(reserved_time=this_hour).exists()

        if is_ordered:
            return False, "RESERVED"

        return True, "FREE"

    def is_day_selectable(self, day):
        today = datetime.date.today()
        day = JalaliDate(year=self.year, month=self.month, day=day, locale="en").to_gregorian()
        diff = (day - today).days
        days_limit = int(functions.get_setting(enums.DefaultSettings.LIMIT_DAYS_FOR_RESERVATION, 7))
        if diff < 0 or diff > days_limit:
            return False
        else:
            return True
