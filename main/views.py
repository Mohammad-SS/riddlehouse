from django.shortcuts import render, HttpResponse
from riddlehouse import MonthBooking
from game import models
import radar
import datetime


# Create your views here.

def index(request):
    models.Exclusion()
    month = MonthBooking.Month(7).create_calander(1)
    return HttpResponse("SALAM !")


def create_test_hour(reqeust):
    room = models.Room.objects.get(pk=1)
    new_exc = models.Exclusion(room=room)
    new_exc.zones = ("2022-10-1", "2022-10-20")

    new_exc.save()
    return HttpResponse("DONE")


def create_test_execs(request):
    game = models.Room.objects.get(id=1)
    for i in range(0, 120000):
        start_time = radar.random_datetime(
            start=datetime.datetime(year=2021, month=1, day=1),
            stop=datetime.datetime(year=2022, month=12, day=20)
        )
        end_time = start_time + datetime.timedelta(hours=2)
        new_exec = models.Exclusion(room=game)
        new_exec.zones = (start_time, end_time)
        new_exec.save()
