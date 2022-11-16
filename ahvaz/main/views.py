import datetime
import random

from django.contrib.auth import authenticate, login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from persiantools import jdatetime
import game.models
from riddlehouse.helpers import enums
from . import models as main_models
from game import models as game_models
from orders import models as order_models
from django.template.defaultfilters import slugify
from django.core.paginator import Paginator
from riddlehouse.helpers import functions
from persiantools import jdatetime


def TESTSMS(request):
    functions.send_sms.delay(order=1)
    print("DONE")


# Create your views here.

class PanelRoomsView(LoginRequiredMixin, View):
    def get(self, request):
        rooms = game_models.Room.objects.all()
        context = {
            "title": "اتاق ها",
            "rooms": rooms
        }
        return render(request, 'panel/manage-rooms/manage-rooms.html', context)

    def post(self, request):
        data = request.POST
        mode = data.get("mode", None)
        room = data.get("room", None)
        hours = data.getlist("hours", [])
        if not room:
            pass
        room = game_models.Room.objects.get(pk=room)
        from_date = data.get("from_date", "1401/01/01")
        to_date = data.get("to_date", "1402/02/02")
        from_date = from_date.split("/")
        to_date = to_date.split("/")
        from_date = jdatetime.JalaliDate(year=int(from_date[0]), month=int(from_date[1]),
                                         day=int(from_date[2])).to_gregorian()
        to_date = jdatetime.JalaliDate(year=int(to_date[0]), month=int(to_date[1]), day=int(to_date[2])).to_gregorian()

        if not mode:
            pass
        weekday = []
        if int(mode) == 1:
            mode = enums.ExclusionsType.DATE
        elif int(mode) == 3:
            mode = enums.ExclusionsType.DATE_AND_WEEKDAY
            weekday = data.getlist("weekday", [])

        fields = {
            "room": room,
            "role": mode,
            "from_date": from_date,
            "to_date": to_date,
            "weekdays": [int(day) for day in weekday],
            "hours": hours,
        }
        exclusion = game_models.Exclusion(**fields)
        exclusion.save()

        return redirect("main:schedule")


class PanelRoomView(LoginRequiredMixin, View):
    def get(self, request):
        return render(request, "panel/manage-rooms/create.html", {})

    def post(self, request):
        data = request.POST
        room_type = data.get("room_type", None)
        picture = request.FILES.get("banner", None)
        if room_type == "box":
            this_type = enums.RoomType.BOX
            price = data.getlist("price", None)
            for package_price in price:
                package_price = int(package_price)
            box_packages_prices = price
            price = None
        elif room_type == "real":
            this_type = enums.RoomType.REAL
            price = data.get("price", None)
            price = int(price)
            box_packages_prices = None
        else:
            this_type = None
            box_packages_prices = None
            price = None
        name = data.get("name", None)
        difficulty = data.get("difficulty", None)
        min_players = data.get("min_players", None)
        max_players = data.get("max_players", None)
        weekdays = data.getlist("weekday", None)
        hours = data.getlist("hours", None)
        hours.sort(key=lambda x: int(x.split(":")[0]))
        warnings = data.get("warnings", None)
        descriptions = data.get("descriptions", None)
        conditions = data.get("conditions", None)
        fields = {
            "name": name,
            "difficulty": difficulty,
            "price_per_unit": price,
            "default_hours": hours,
            "warnings": warnings,
            "min_players": min_players,
            "max_players": max_players,
            "description": descriptions,
            "conditions": conditions,
            "default_days": weekdays,
            "room_type": this_type,
            "box_packages_prices": box_packages_prices,
        }
        room = game_models.Room(**fields)
        room.banner = picture
        room.save()
        return redirect("main:rooms")


class PanelCoupanView(LoginRequiredMixin, View):
    def get(self, request):
        coupons = order_models.Coupon.objects.all()
        rooms = game_models.Room.objects.all()
        context = {
            "coupons": coupons,
            "title": "کد های تخفیف",
            "rooms": rooms
        }
        return render(request, 'panel/coupan/coupan.html', context)

    def post(self, request):
        data = request.POST
        code = data.get("code")
        code = slugify(code)
        does_code_exists = order_models.Coupon.objects.filter(code=code).exists()
        if does_code_exists:
            return redirect("main:coupans")
        price = data.get("price")
        max_number = data.get("max_number")
        rooms = data.getlist("room", None)
        code_type = data.get("type", None)
        if code_type == "constant":
            code_type = enums.CouponsType.CONSTANT
        elif code_type == "percentage":
            code_type = enums.CouponsType.PERCENTAGE
        else:
            code_type = None

        fields = {
            "code": code,
            "amount": price,
            "type": code_type,
            "capacity": max_number
        }
        this_coupon = order_models.Coupon(**fields)
        this_coupon.save()
        for room in rooms:
            this_room = game_models.Room.objects.get(pk=room)
            this_coupon.available_rooms.add(this_room)
        this_coupon.save()
        return redirect("main:coupans")


class PanelOrderView(LoginRequiredMixin, View):
    def get(self, request):
        # filters
        page_number = request.GET.get('page', 1)
        data = request.GET
        rooms = game_models.Room.objects.all()
        min_date = None
        max_date = None
        if data.get("min_date", None):
            min_date = data.get("min_date", "").split("/")
            min_date = jdatetime.JalaliDate(year=int(min_date[0]), month=int(min_date[1]),
                                            day=int(min_date[2])).to_gregorian()

        if data.get("max_date", None):
            max_date = data.get("max_date", "").split("/")
            max_date = jdatetime.JalaliDate(year=int(max_date[0]), month=int(max_date[1]),
                                            day=int(max_date[2])).to_gregorian()

        mood = data.get("filter_mode", "reserve")
        mood_name = {}
        if mood == "payment":
            mood_name["min"] = "created_date__gte"
            mood_name["max"] = "created_date__lte"
        else:
            mood_name["min"] = "reserved_time__gte"
            mood_name["max"] = "reserved_time__lte"

        filters = {
            "room__id": data.get("room", None),
            mood_name["min"]: min_date,
            mood_name["max"]: max_date
        }

        filters = functions.remove_nones(filters)
        orders = order_models.Order.objects.filter(**filters).order_by("-id")
        paginator = Paginator(orders, 15)
        page_obj = paginator.get_page(page_number)

        context = {
            "orders": page_obj,
            "rooms": rooms,
            "title": "سفارش ها",
            "order_count": len(orders)

        }

        return render(request, 'panel/order/orders.html', context)

    def post(self, request):
        data = request.POST
        room = data.get("room_id", None)
        room = get_object_or_404(game_models.Room, pk=room)
        phone = data.get("phone", "")
        date = data.get("date", "0/0/0")
        name = data.get("name", "")
        hour = data.get("hour", "00:00")
        date = date.split("/")
        hour = hour.split(":")
        reserved_time = jdatetime.JalaliDateTime(year=int(date[0]), month=int(date[1]), day=int(date[2]),
                                                 hour=int(hour[0]), minute=int(hour[1])).to_gregorian()
        fields = {
            "room": room,
            "customer_name": name,
            "customer_number": phone,
            "paid": 0,
            "transaction_number": "رزرو حضوری",
            "key": random.randint(1000, 9999),
            "reserved_time": reserved_time
        }
        order_object = order_models.Order(**fields)
        order_object.save()
        functions.send_sms.delay(order=order_object.pk)
        return redirect("main:orders")


class PanelScheduleView(LoginRequiredMixin, View):

    def get(self, request):
        exclusions = game_models.Exclusion.objects.all().order_by("-pk")
        context = {
            "exclusions": exclusions,
            "title": "زمان بندی ها"
        }
        return render(request, "panel/schedule/schedule.html", context)


class LandingView(View):
    def get(self, request):
        rooms = game_models.Room.objects.filter(room_type=enums.RoomType.REAL)
        last_box = game_models.Room.objects.filter(room_type=enums.RoomType.BOX).last()
        return render(request, 'main/landing.html', {"rooms": rooms, "box": last_box})


class LoginView(View):

    def get(self, request):
        if request.user.id:
            return redirect("main:rooms")
        context = {
            "title": "ورود به خانه معما",
        }
        return render(request, "panel/login.html", context)

    def post(self, request):
        data = request.POST
        username = data.get("username", None)
        password = data.get("password", None)
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect("main:rooms")
        else:
            return redirect("main:login")


class RoomView(View):
    def get(self, request, pk):
        rooms = game.models.Room.objects.all()
        room = game_models.Room.objects.get(pk=pk)
        now = datetime.datetime.now().strftime("%Y/%m/%d")
        context = {
            "rooms": rooms,
            "room": room,
            "title": room.name,
            "now": now
        }
        return render(request, 'main/reserveroom.html', context)

    def post(self, request, pk):
        data = request.POST
        room = game_models.Room.objects.get(pk=pk)

        date = data.get("date", None)
        turn = data.get("turn", None)
        package = data.get("package", None)
        if room.room_type == enums.RoomType.REAL:
            if not date or not turn:
                return False
            hour, minutes = turn.split(":")
        else:
            if not package:
                return False
            hour = 12
            minutes = 0

        year, month, day = date.split("/")
        reserved_date = jdatetime.JalaliDateTime(int(year), int(month), int(day), int(hour),
                                                 int(minutes)).to_gregorian()
        fields = {
            "amount": data.get("price", None),
            "room_id": pk,
            "customer_name": data.get('name', None),
            "package": package,
            "mobile": data.get('phone', None),
            "players_number": data.get('persons', None),
            "coupon": data.get('coupon', None),
            "reserved_time": reserved_date,
        }
        payment = functions.start_payment(**fields)
        if payment.get("valid", None):
            return redirect(payment.get("url"))
        else:
            return redirect("main:room-page", pk=pk)


class RemoveCoupon(LoginRequiredMixin, View):

    def post(self, request, pk):
        coupon = order_models.Coupon.objects.get(pk=pk)
        coupon.delete()
        return redirect("main:coupans")


class PanelSettingsView(LoginRequiredMixin, View):
    def get(self, request):
        _settings = [e for e in enums.DefaultSettings]
        settings = dict()
        for setting in _settings:
            settings[setting.name] = dict()
            settings[setting.name]["slug"] = setting.value['slug']
            settings[setting.name]["name"] = setting.name
            settings[setting.name]["value"] = functions.get_setting(setting)
        print(settings)
        context = {
            "title": "تنظیمات",
            "settings": settings
        }
        return render(request, 'panel/settings.html', context)

    def post(self, request):
        data = request.POST.copy()
        data.pop("csrfmiddlewaretoken")

        for key, setting in data.items():
            name = key.upper()
            functions.set_setting(name, setting)

        return redirect("main:settings")


class PanelRoomEditView(LoginRequiredMixin, View):

    def get(self, request, pk):
        room = game_models.Room.objects.get(pk=pk)
        context = {
            "room": room,
            "title": "ویرایش اتاق",
        }
        return render(request, "panel/manage-rooms/edit.html", context)

    def post(self, request, pk):
        room = game_models.Room.objects.filter(pk=pk)
        data = request.POST
        room_type = data.get("room_type", None)
        picture = request.FILES.get("banner", None)
        if room_type == "box":
            this_type = enums.RoomType.BOX
            price = data.getlist("price", None)
            for package_price in price:
                package_price = int(package_price)
            box_packages_prices = price
            price = None
        elif room_type == "real":
            this_type = enums.RoomType.REAL
            price = data.get("price", None)
            price = int(price)
            box_packages_prices = None
        else:
            this_type = None
            box_packages_prices = None
            price = None
        name = data.get("name", None)
        difficulty = data.get("difficulty", None)
        min_players = data.get("min_players", None)
        max_players = data.get("max_players", None)
        weekdays = data.getlist("weekday", None)
        hours = data.getlist("hours", None)
        hours.sort(key=lambda x: int(x.split(":")[0]))
        warnings = data.get("warnings", None)
        descriptions = data.get("descriptions", None)
        conditions = data.get("conditions", None)
        fields = {
            "name": name,
            "difficulty": difficulty,
            "price_per_unit": price,
            "default_hours": hours,
            "warnings": warnings,
            "min_players": min_players,
            "max_players": max_players,
            "description": descriptions,
            "conditions": conditions,
            "default_days": weekdays,
            "room_type": this_type,
            "box_packages_prices": box_packages_prices,
        }
        fields = functions.remove_empties(fields)
        room.update(**fields)
        room[0].banner = picture
        room[0].save()
        return redirect("main:rooms")


class ReserveCompleted(View):

    def get(self, request):
        rooms = game_models.Room.objects.filter(room_type=enums.RoomType.REAL)
        order_status = functions.verify_payment(request.GET.get("Authority"))
        try:
            room = order_status.get("payment", None).room
        except Exception:
            room = None

        context = {
            "order_status": order_status,
            "payment": order_status.get("payment", None),
            "room": room,
            "order": order_status.get("order", None),
            "title": "نتیجه پرداخت",
            "rooms": rooms,
        }
        return render(request, "main/reserveroom.html", context)
