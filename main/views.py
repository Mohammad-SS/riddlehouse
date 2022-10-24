from django.shortcuts import render
from django.views import View

import game.models
from riddlehouse.helpers import enums
from . import models as main_models
from game import models as game_models


# Create your views here.


class LandingView(View):
    def get(self, request):
        rooms = game_models.Room.objects.filter(room_type=enums.RoomType.REAL)
        last_box = game_models.Room.objects.filter(room_type=enums.RoomType.BOX).last()
        return render(request, 'main/landing.html', {"rooms": rooms, "box": last_box})


class RoomView(View):
    def get(self, request, pk):
        rooms = game.models.Room.objects.all()
        room = game_models.Room.objects.get(pk=pk)
        context = {
            "rooms": rooms,
            "room": room,
            "title": room.name,
        }
        return render(request, 'main/reserveroom.html', context)
