import datetime
import random
import pytz
from django.core.exceptions import ObjectDoesNotExist
from persiantools.jdatetime import JalaliDate, JalaliDateTime
from . import serializers
from game import models
from riddlehouse.helpers import enums
from riddlehouse.helpers import functions
from django.db.models import Q

def check_vip(timestamp, room):
    dt = datetime.datetime.fromtimestamp(timestamp)
    # Get the weekday (0 = Monday, 6 = Sunday)
    weekday = dt.weekday() + 1

    # Get the date in the format YYYY-MM-DD
    date = dt.strftime('%Y-%m-%d')

    # Get the time in the format HH:MM:SS
    time = dt.strftime('%H:%M')

    vip_sans = models.VipSans.objects.filter(
        Q(room=room) & (
            Q(from_date__lte=dt.date(), to_date__gte=dt.date()) | Q(weekdays__contains=[weekday])
        )
    )


    # print("--------------------------------------")
    # print(vip_sans)
    # print("--------------------------------------")
    
    return vip_sans.exists()

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

    def create_calendar(self, room_id=None):
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
            this_day["selectable"] = self.is_day_selectable(day, room)
            this_day['times'] = self.get_this_day_times(day, room)
            calendar[week_num][day] = this_day
        return calendar

    def get_this_day_times(self, day, room):
        hours = dict()
        this_day = JalaliDate(self.year, self.month, day, locale="fa")
        this_day_hours = self.get_role_hours(this_day, room)
        if not this_day.isoweekday() in room.default_days:
            return hours
        for hour in this_day_hours:
            this_hour, this_minutes = hour.split(":")
            this_timestamp = JalaliDateTime(self.year, self.month, day, int(this_hour),
                                            int(this_minutes)).timestamp()
            
            is_vip = self.check_vip(this_timestamp, room)
            hours[hour] = dict()
            hours[hour]["is_vip"] = is_vip
            hours[hour]["timestamp"] = this_timestamp
            hours[hour]['is_reservable'], hours[hour]['status'] = self.check_hour(this_timestamp, room)
            hours[hour]['rand_id'] = "_{}".format(random.randint(10000, 99999))
        return hours

    @classmethod
    def check_hour(cls, timestamp, room: models.Room):
        this_hour = datetime.datetime.fromtimestamp(timestamp)

        is_ordered = room.orders.filter(reserved_time__gte=this_hour - datetime.timedelta(minutes=30),
                                        reserved_time__lte=this_hour + datetime.timedelta(minutes=30)).exists()

        if is_ordered:
            return False, "RESERVED"

        if datetime.datetime.now() + datetime.timedelta(minutes=45) > this_hour:
            # print(datetime.datetime.now() , datetime.datetime.now() - datetime.timedelta(minutes=45) , this_hour )
            # print(this_hour.strftime("H:i"))
            return False, "PASSED"

        ote = room.otes.filter(date_time=this_hour).order_by("-id")
        if ote.exists():
            ote = ote[0]
            if ote.closed:
                return False, "CLOSED"
        return True, "FREE"

    def is_day_selectable(self, day, room):
        today = datetime.date.today()
        day = JalaliDate(year=self.year, month=self.month, day=day, locale="en").to_gregorian()
        diff = (day - today).days
        if room.room_type == enums.RoomType.BOX:
            start_days = 4
        else:
            start_days = 0

        days_limit = int(functions.get_setting(enums.DefaultSettings.LIMIT_DAYS_FOR_RESERVATION, 7))
        if diff < start_days or diff > days_limit:
            return False
        else:
            return True

    @classmethod
    def get_role_hours(cls, day, room):
        _day = day.to_gregorian()
        date = datetime.date(_day.year, _day.month, _day.day)
        exclusions = room.exclusions.filter(from_date__lte=date, to_date__gte=date)

        if not exclusions.exists():
            return room.default_hours
        exclusion = exclusions.last()
        exclusion_hours = cls.get_execution_hours(exclusion, day)
        return exclusion_hours

    @classmethod
    def get_execution_hours(cls, exclusion, day):
        if exclusion.role == enums.ExclusionsType.DATE_AND_WEEKDAY:
            if day.isoweekday() in exclusion.weekdays:
                return exclusion.hours
            else:
                return exclusion.room.default_hours
        elif exclusion.role == enums.ExclusionsType.DATE:
            return exclusion.hours
        else:
            return exclusion.room.default_hours


class RoomWeek():
    week_range = 7

    def __init__(self):
        self.rooms = models.Room.objects.all()
        self.today = datetime.date.today()
        rooms = self.create_rooms_list()

    def create_rooms_list(self):
        rooms = dict()
        for room in self.rooms:
            this_room = {
                "room_obj": serializers.GameSerializer(room).data,
                "calendar": self.create_room_calendar(room)
            }
            rooms[room.id] = this_room
        return rooms

    def create_room_calendar(self, room):
        days = list()
        for day in range(0, self.week_range):
            this_day = self.today + datetime.timedelta(days=day)
            jalali_day = JalaliDate(this_day)
            this_day = {
                "date": jalali_day.strftime("%Y/%m/%d"),
                "weekday": jalali_day.isoweekday(),
                "hours": self.get_this_day_times(jalali_day, room)
            }
            days.append(this_day)

        return days

    def check_vip(self, timestamp, room):
        dt = datetime.datetime.fromtimestamp(timestamp)
        # Get the weekday (0 = Monday, 6 = Sunday)
        weekday = dt.weekday() + 1

        # Get the date in the format YYYY-MM-DD
        date = dt.strftime('%Y-%m-%d')

        # Get the time in the format HH:MM:SS
        time = dt.strftime('%H:%M')

        vip_sans = models.VipSans.objects.filter(
            Q(room=room) & (
                Q(from_date__lte=dt.date(), to_date__gte=dt.date()) | Q(weekdays__contains=[weekday])
            )
        )


        print("--------------------------------------")
        print(vip_sans)
        print("--------------------------------------")
        
        return vip_sans.exists()

    def get_this_day_times(self, day, room):
        hours = dict()

        this_day_hours = Month.get_role_hours(day, room)

        if not day.isoweekday() in room.default_days:
            return hours
        

        for hour in this_day_hours:
            this_hour, this_minutes = hour.split(":")
            this_timestamp = JalaliDateTime(day.year, day.month, day.day, int(this_hour),
                                            int(this_minutes)).timestamp()
            is_vip = self.check_vip(this_timestamp, room)
            hours[hour] = dict()
            hours[hour]["is_vip"] = is_vip
            hours[hour]["timestamp"] = this_timestamp
            hours[hour]['is_reservable'], hours[hour]['status'] = Month.check_hour(this_timestamp, room)
            hours[hour]["order"] = self.get_order_object(this_timestamp, room)
            hours[hour]['rand_id'] = "_{}".format(random.randint(10000, 99999))
        return hours

    def get_order_object(self, timestamp, room):
        this_hour = datetime.datetime.fromtimestamp(timestamp)

        order = room.orders.filter(reserved_time__gt=this_hour - datetime.timedelta(minutes=30),
                                   reserved_time__lt=this_hour + datetime.timedelta(minutes=30))

        if not order.exists():
            return None
        else:
            return serializers.OrderSerializer(order[0]).data
