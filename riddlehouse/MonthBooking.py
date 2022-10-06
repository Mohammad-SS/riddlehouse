import time

from persiantools.jdatetime import JalaliDate, JalaliDateTime
from game import models
from orders import models as orders_model
import datetime


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
        for day in range(1, self.month_range + 1):
            this_day = dict()
            this_weekday = JalaliDate(self.year, self.month, day).isoweekday()

            if this_weekday == 1 and not day == 1:
                week_num += 1
                calendar[week_num] = dict()
            this_day["weekday"] = this_weekday
            this_day['times'] = self.get_this_day_times(day, room_id)
            calendar[week_num][day] = this_day
        return calendar

    def get_this_day_times(self, day, room_id):
        hours = dict()
        this_day = JalaliDate(self.year, self.month, day, locale="fa")
        room = models.Room.objects.get(id=room_id)
        if not this_day.isoweekday() in room.default_days:
            return hours
        for hour in room.default_hours:
            this_hour, this_minutes = hour.split(":")
            this_timestamp = JalaliDateTime(self.year, self.month, day, int(this_hour),
                                            int(this_minutes)).timestamp()
            hours[hour] = dict()
            hours[hour]["timestamp"] = this_timestamp
            hours[hour]['is_reservable'] , hours[hour]['status'] = self.check_hour(this_timestamp, room)
        return hours

    @classmethod
    def check_hour(cls, timestamp, room: models.Room):
        # check ORDERS DATABASE
        this_hour = datetime.datetime.fromtimestamp(timestamp)
        t = time.time()
        is_excluded = room.exclusions.filter(zones__contains=this_hour).exists()
        t = time.time() - t
        print(t)
        if is_excluded:
            return False, "CLOSED"

        is_ordered = room.orders.filter(reserved_time=this_hour).exists()

        if is_ordered:
            return False, "RESERVED"

        return True, "FREE"
