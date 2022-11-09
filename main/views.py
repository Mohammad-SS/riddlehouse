import datetime

from django.shortcuts import render, redirect
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


# Create your views here.

class PanelRoomsView(View):
    def get(self, request):
        rooms = game_models.Room.objects.all()
        context = {
            "title": "اتاق ها",
            "rooms": rooms
        }
        return render(request, 'panel/manage-rooms/manage-rooms.html', context)


class PanelRoomView(View):
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


class PanelCoupanView(View):
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


class PanelOrderView(View):
    def get(self, request):
        # filters
        page_number = request.GET.get('page', 1)

        rooms = game_models.Room.objects.all()
        orders = order_models.Order.objects.all()
        paginator = Paginator(orders, 15)
        page_obj = paginator.get_page(page_number)
        print(page_obj.__dict__)
        context = {
            "orders": page_obj,
            "rooms": rooms,
            "title": "سفارش ها",
            "order_count": len(orders)

        }

        return render(request, 'panel/order/orders.html', context)

    def post(self, request):
        data = request.POST
        print(data)


class PanelScheduleView(View):
    template_name = 'panel/schedule/schedule.html'

    def get(self, request):
        return render(request, self.template_name, {})


class LandingView(View):
    def get(self, request):
        rooms = game_models.Room.objects.filter(room_type=enums.RoomType.REAL)
        last_box = game_models.Room.objects.filter(room_type=enums.RoomType.BOX).last()
        return render(request, 'main/landing.html', {"rooms": rooms, "box": last_box})


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
        package = data.get("package" , None)
        if room.room_type==enums.RoomType.REAL:
            if not date or not turn:
                return False
            hour, minutes = turn.split(":")
        else:
            if not package:
                return False
            hour = 0
            minutes = 0

        year, month, day = date.split("/")
        reserved_date = jdatetime.JalaliDateTime(int(year), int(month), int(day), int(hour), int(minutes)).to_gregorian()
        fields = {
            "amount": data.get("price", None),
            "room_id": pk,
            "customer_name": data.get('name', None),
            "package" : package ,
            "mobile": data.get('phone', None),
            "players_number": data.get('persons', None),
            "coupon": data.get('coupon', None),
            "reserved_time": reserved_date,
        }
        payment = functions.start_payment(**fields)
        if payment.get("valid" , None) :
            return redirect(payment.get("url"))
        else:
            return redirect("main:room-page" , pk=pk)


class RemoveCoupon(View):

    def post(self, request, pk):
        coupon = order_models.Coupon.objects.get(pk=pk)
        coupon.delete()
        return redirect("main:coupans")


class PanelSettingsView(View):
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


class PanelRoomEditView(View):

    def get(self, request, pk):
        room = game_models.Room.objects.get(pk=pk)
        context = {
            "room": room,
            "title": "ویرایش اتاق",
        }
        return render(request, "", context)


class ReserveCompleted(View):

    def get(self,request):
        payment = functions.verify_payment(request.GET.get("Authority"))
        context = {
            "payment" : payment,
            "title" : "نتیجه پرداخت",
        }
        return render(request,"TEMPLATE",context)
