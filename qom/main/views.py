import datetime
import random, json
from dateutil import parser
from django.db.models import Q
from django.contrib.auth import authenticate, login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.utils.http import urlencode
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
import pytz
from riddlehouse import MonthBooking
from pprint import pprint
from django.contrib.auth.models import User
from .base_views import ActionBaseView
from django.contrib import messages
from orders.merchants.zarinpal_merchant import ZarinpalMerchant
from orders.merchants.pec_merchant import PecMerchant
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt

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
        vip_setter = data.get("vip_set", None)
        hours = data.getlist("hours", [])
        if not room:
            pass
        room = game_models.Room.objects.get(pk=room)
        from_date = data.get("from_date", "1401/01/01")
        to_date = data.get("to_date", "1402/02/02")
        if bool(from_date) and bool(to_date):
            from_date = from_date.split("/")
            to_date = to_date.split("/")
            from_date = jdatetime.JalaliDate(year=int(from_date[0]), month=int(from_date[1]),
                                            day=int(from_date[2])).to_gregorian()
            to_date = jdatetime.JalaliDate(year=int(to_date[0]), month=int(to_date[1]), day=int(to_date[2])).to_gregorian()

        if not mode:
            pass


        weekday = []
        if mode:
            if int(mode) == 1:
                mode = enums.ExclusionsType.DATE
            elif int(mode) == 3:
                mode = enums.ExclusionsType.DATE_AND_WEEKDAY
                weekday = data.getlist("weekday", [])
        else:
            weekday = data.getlist("weekday", [])

        fields = {
            "room": room,
            "role": mode,
            "from_date": from_date if bool(from_date) else None,
            "to_date": to_date if bool(to_date) else None,
            "weekdays": [int(day) for day in weekday],
            "hours": hours,
        }

        if vip_setter is not None:
            fields.pop('role')
            price_per_unit = data.get("price_per_unit", room.price_per_unit)
            pre_pay = data.get("pre_pay", room.pre_pay)

            fields.update({
                "price_per_unit": price_per_unit,
                "pre_pay" : pre_pay
            })

            vip_sans = game_models.VipSans(**fields)
            vip_sans.save()
        else:
            exclusion = game_models.Exclusion(**fields)
            exclusion.save()

        
        return redirect("main:schedule")


class PanelOverview(LoginRequiredMixin, View):
    def get(self, request):
        calendar = MonthBooking.RoomWeek().create_rooms_list()
        pritable = [value.get('calendar') for key,value in calendar.items()]
      
        # with open("data.json", 'a+', encoding="utf-8") as file:
        #     file.write(json.dumps(pritable))
        #     file.close()
        context = {
            "title": "تقویم",
            "calendar": calendar,
        }
        return render(request, "panel/overview.html", context)

    def post(self, request):
        data = request.POST
    
        if data.get("action", "reserve") == "close":
        
            room_id = data.get("room", None)
            date = data.get("date", None)
            time = data.get("time", None)
            if not room_id or not date or not time:
                return None
            date = date.split("/")
            time = time.split(":")
            print(date, time)
            date_time = jdatetime.JalaliDateTime(year=int(date[0]), month=int(date[1]), day=int(date[2]),
                                                 hour=int(time[0]), minute=int(time[1])).to_gregorian()
            # date_time = pytz.timezone("Asia/Tehran").localize(date_time)
            game_models.OneTimeExclusion(room_id=room_id, date_time=date_time, closed=True).save()
            return redirect("main:reserve_calendar")
        if data.get("action", "reserve") == "open":
            room_id = data.get("room", None)
            date = data.get("date", None)
            time = data.get("time", None)
            if not room_id or not date or not time:
                return None
            date = date.split("/")
            time = time.split(":")
            date_time = jdatetime.JalaliDateTime(year=int(date[0]), month=int(date[1]), day=int(date[2]),
                                                 hour=int(time[0]), minute=int(time[1])).to_gregorian()
            #date_time = pytz.timezone("Asia/Tehran").localize(date_time)
            game_models.OneTimeExclusion.objects.filter(room_id=room_id, date_time=date_time).delete()
            return redirect("main:reserve_calendar")

        room = data.get("room_id", None)
        room = get_object_or_404(game_models.Room, pk=room)
        phone = data.get("phone", "")
        players_number = data.get("players", 0)
        price = data.get("price", 0)
        date = data.get("date", "0/0/0")
        description = data.get("descriptions", "")
        name = data.get("name", "")
        hour = data.get("hour", "00:00")
        date = date.split("/")
        hour = hour.split(":")
        reserved_time = jdatetime.JalaliDateTime(year=int(date[0]), month=int(date[1]), day=int(date[2]),
                                                 hour=int(hour[0]), minute=int(hour[1])).to_gregorian()
        # reserved_time = pytz.timezone("Asia/Tehran").localize(reserved_time)
        fields = {
            "room": room,
            "customer_name": name,
            "customer_number": phone,
            "paid": price,
            "description": description,
            "players_number": players_number,
            "transaction_number": "رزرو حضوری",
            "key": random.randint(1000, 9999),
            "reserved_time": reserved_time
        }
        order_object = order_models.Order(**fields)
        order_object.save()
        functions.send_sms.delay(order=order_object.pk)
        return redirect("main:reserve_calendar")


class VipSansView(LoginRequiredMixin, View):
    
    def redirect_to_overview(self):
        return redirect(reverse('main:reserve_calendar'))


    def create_new_one_time_vip_sans(self, data, exclude=False):
        obj = game_models.OneTimeVipSans.objects.create(**data)
        return obj


    def post(self, requset):
        data = requset.POST
        print(data)
        # return self.redirect_to_overview()
        data_dict = {key:data.get(key) for key in ['room_id', 'date', 'hour', 'price_per_unit', 'pre_pay', 'action', 'is_vip']}

        if not all(data_dict.values()):
           return self.redirect_to_overview()
        
        jalali_date_str = str(parser.parse("%s %s" % (data_dict.get('date'), data_dict.get('hour'))))
        jalali_date = jdatetime.JalaliDateTime.strptime(jalali_date_str, "%Y-%m-%d %H:%M")
        date =jalali_date.to_gregorian()
     
        room = game_models.Room.objects.filter(id=data_dict['room_id'])
        if not room.exists():
            return self.redirect_to_overview()

        room = room.last()
        one_time = game_models.OneTimeVipSans.objects.filter(room=room, date_time=date)
        is_vip_sans = game_models.VipSans.objects.filter(Q(room=room) and (Q(from_date__lte=date, to_date__gte=date) | Q(weekdays__contains=[jalali_date.weekday()+1])))
        print(date)
        print(date.weekday())
        print(jalali_date.weekday())
        print(is_vip_sans)
        action = data_dict['action']
        if action == 'set':
            self.create_new_one_time_vip_sans(
                data={
                    "room": room,
                    "date_time": date,
                    "price_per_unit": data_dict['price_per_unit'],
                    "pre_pay": data_dict['pre_pay'],
                    "exclude": True if data_dict['is_vip'] == 'yes' else False
                }
            )

            return self.redirect_to_overview()
        
        if action == 'update':
            if one_time.exists():
                one_time = one_time.last()
                one_time.price_per_unit = data_dict['price_per_unit']
                one_time.pre_pay = data_dict['pre_pay']
                one_time.exclude = False
                one_time.save() 
            else:
                self.create_new_one_time_vip_sans(
                    data={
                        "room": room,
                        "date_time": date,
                        "price_per_unit": data_dict['price_per_unit'],
                        "pre_pay": data_dict['pre_pay'],
                        "exclude": False
                    }
                )
            
            return self.redirect_to_overview()

        if action == 'delete':
            if one_time.exists():
                one_time.delete()
                
                if is_vip_sans.exists():
                    self.create_new_one_time_vip_sans(
                        data={
                            "room": room,
                            "date_time": date,
                            "price_per_unit": data_dict['price_per_unit'],
                            "pre_pay": data_dict['pre_pay'],
                            "exclude": True
                        }
                )

            else:
                 self.create_new_one_time_vip_sans(
                    data={
                        "room": room,
                        "date_time": date,
                        "price_per_unit": data_dict['price_per_unit'],
                        "pre_pay": data_dict['pre_pay'],
                        "exclude": True
                    }
                )
                 
            return self.redirect_to_overview()

        return self.redirect_to_overview()
        # if data_dict['action'] == "delete":
        #     if one_time.exists():
        #         one_time = one_time.last()
        #         one_time.delete()
        #     else:
        #         self.create_new_one_time_vip_sans(
        #             data={
        #                 "room": room,
        #                 "date_time": date,
        #                 "price_per_unit": data_dict['price_per_unit'],
        #                 "pre_pay": data_dict['pre_pay'],
        #                 "exclude": True if data_dict['is_vip'] == 'yes' else False
        #             }
        #         )
        # elif data_dict['action'] == "set":
        #     if one_time.exists():
                # one_time = one_time.last()
                # one_time.price_per_unit = data_dict['price_per_unit']
                # one_time.pre_pay = data_dict['pre_pay']
                # one_time.exclude = False
                # one_time.save()
        #     elif data_dict['is_vip'] == 'no':
        #         self.create_new_one_time_vip_sans(
        #             data={
        #                 "room": room,
        #                 "date_time": date,
        #                 "price_per_unit": data_dict['price_per_unit'],
        #                 "pre_pay": data_dict['pre_pay'],
        #                 "exclude": False
        #             }
        #         )

        # return self.redirect_to_overview()


class PanelRoomView(LoginRequiredMixin, View):
    def get(self, request):
        return render(request, "panel/manage-rooms/create.html", {})

    def post(self, request):
        data = request.POST
        img_alt = data.get('img-alt', "")
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
            box_packages_prices = [0, 0]
        else:
            this_type = None
            box_packages_prices = None
            price = None
        name = data.get("name", None)
        difficulty = data.get("difficulty", None)
        min_players = data.get("min_players", None)
        max_players = data.get("max_players", None)
        weekdays = data.getlist("weekday", None)
        game_duration = data.get("duration", "")
        admin_phones = data.get("admin_phones", None)
        merchant = data.get("merchant",None)
        if not admin_phones:
            admin_phones = functions.get_setting(enums.DefaultSettings.MAX_SMS_ADMIN_NUMBER)
        hours = data.getlist("hours", None)
        hours.sort(key=lambda x: int(x.split(":")[0]))
        warnings = data.get("warnings", None)
        descriptions = data.get("descriptions", None)
        pre_pay = data.get("pre_pay", None)
        conditions = data.get("conditions", None)
        fields = {
            "slug": functions.slugify(name),
            "name": name,
            "difficulty": difficulty,
            "price_per_unit": price,
            "pre_pay": pre_pay,
            "default_hours": hours,
            "game_duration": game_duration,
            "warnings": warnings,
            "min_players": min_players,
            "max_players": max_players,
            "description": descriptions,
            "conditions": conditions,
            "default_days": weekdays,
            "room_type": this_type,
            "admin_phones": admin_phones,
            "google_map": data.get("google_map", ""),
            "balad_link": data.get("balad_link", ""),
            "box_packages_prices": box_packages_prices,
            "img_alt": img_alt,
            "merchant" : merchant,
        }
        fields = functions.remove_empties(fields)
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

    def post(self, request):
        order_id = request.POST.get("delete", None)
        try:
            order_models.Order.objects.get(id=order_id).delete()
        except Exception:
            pass
        return redirect("main:orders")

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


class PanelScheduleView(LoginRequiredMixin, View):

    def get(self, request):
        exclusions = game_models.Exclusion.objects.all().order_by("-pk")
        otes = game_models.OneTimeExclusion.objects.filter(date_time__gte=datetime.date.today()).order_by("-pk")
        vipsans = game_models.VipSans.objects.filter(Q(to_date__gte=datetime.date.today()) | Q(to_date__isnull=True) | Q(from_date__isnull=True)).order_by("-pk")
        otvip = game_models.OneTimeVipSans.objects.filter(date_time__gte=datetime.date.today()).order_by("-pk")
        context = {
            "exclusions": exclusions,
            "vipsans" : vipsans,
            "otes": otes,
            "otvip": otvip,
            "title": "زمان بندی ها"
        }
        return render(request, "panel/schedule/schedule.html", context)


class PanelRemoveSchedule(LoginRequiredMixin, View):

    def get(self, request, pk):
        exclusion = game_models.Exclusion.objects.get(pk=pk)
        exclusion.delete()
        return redirect("main:schedule")

class PanelRemoveVipSchedule(LoginRequiredMixin, View):

    def get(self, request, pk):
        vip = game_models.VipSans.objects.get(pk=pk)
        one_time_vip = game_models.OneTimeVipSans.objects.filter(room=vip.room, date_time__date__range=(vip.from_date, vip.to_date))
        if one_time_vip.exists():
            one_time_vip.delete()
        vip.delete()
        return redirect("main:schedule")


class CitySelectView(View):
    def get(self, request):
        return render(request, 'main/city-select.html', {})


class LandingView(View):
    def get(self, request):
        if request.user.is_authenticated and request.user.username == 'developer':
            rooms = game_models.Room.objects.filter(room_type=enums.RoomType.REAL)
        else:
            rooms = game_models.Room.objects.filter(room_type=enums.RoomType.REAL, is_archive=False)
            
            
        last_box = game_models.Room.objects.filter(room_type=enums.RoomType.BOX, is_archive=False).last()
        context = {
            "rooms": rooms, "box": last_box,
            "title": "خانه معما",
            "meta_description": "خانه معما، به عنوان نخستین مجموعه ی طراحی و اجرای بازی های فکری گروهی اتاق فرار در استان قم، با طراحی و مدیریت سید مهدی شمس الدینی از پاییز 1396 فعالیت خودش را آغاز کرد.",
            "meta_keywords": "خانه معما,اتاق فرار,اتاق فرار قم,اتاق ساواک,فرار از آلکاتراز,فرار از موزه,بازی گروهی قم"
        }
        return render(request, 'main/landing.html', context)


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
    def get(self, request, slug):
        rooms = game_models.Room.objects.filter(room_type=enums.RoomType.REAL, is_archive=False)
        error = request.GET.get("error", None)
        room_filter = {"slug": slug}
        if not request.user.is_authenticated:
            room_filter.update({"is_archive": False})
        room = get_object_or_404(game_models.Room, **room_filter)
        # room = game_models.Room.objects.get(slug=slug)
        now = datetime.datetime.now().strftime("%Y/%m/%d")
        try:
            meta_description = room.description[:155] + "..."
        except Exception:
            meta_description = "اولین اتاق فرار استان قم"
        context = {
            "error": error,
            "rooms": rooms,
            "room": room,
            "meta_description": meta_description,
            "meta_keywords": "خانه معما , اتاق فرار , اسکیپ روم قم ," + room.name,
            "title": room.name,
            "now": now
        }
        return render(request, 'main/reserveroom.html', context)

    def post(self, request, slug):
        data = request.POST
        room_filter = {"slug": slug}
        if not request.user.is_authenticated:
            room_filter.update({"is_archive": False})
        room = get_object_or_404(game_models.Room, slug=slug, is_archive=False)

        date = data.get("date", None)
        turn = data.get("turn", None)
        package = data.get("package", None)
        if room.room_type == enums.RoomType.REAL:
            if not date or not turn:
                return False
            hour, minutes = turn.split(":")
            rest_payment = room.price_per_unit * int(data.get('persons', room.min_players)) - int(
                data.get("pre_pay", room.pre_pay))
            
            is_vip = data.get('is_vip', False)
            if bool(is_vip):
                try:
                    amount = game_models.VipSans.objects.get(pk=is_vip, room=room).pre_pay
                except Exception as e:
                    amount = room.pre_pay
            else:
                amount = room.pre_pay
            
        else:
            if not package:
                return False
            hour = 12
            minutes = 0
            rest_payment = 0
            amount = data.get("package_price", 0)

        year, month, day = date.split("/")
        reserved_date = jdatetime.JalaliDateTime(int(year), int(month), int(day), int(hour),
                                                 int(minutes)).to_gregorian()
        fields = {
            "amount": amount,
            "rest_payment": rest_payment,
            "room_id": room.pk,
            "customer_name": data.get('name', None),
            "package": package,
            "mobile": data.get('phone', None),
            "players_number": data.get('persons', None),
            "coupon": data.get('coupon', None),
            "reserved_time": reserved_date,
        }
        is_ordered, is_in_payment = functions.check_hour_in_use(room.id, reserved_date)

        if is_ordered or is_in_payment:
            rooms = game_models.Room.objects.filter(is_archive=False)
            now = datetime.datetime.now().strftime("%Y/%m/%d")

            try:
                meta_description = room.description[:155] + "..."
            except Exception:
                meta_description = "اولین اتاق فرار استان قم"

            if is_in_payment:
                error = 1
            elif is_ordered:
                error = 2
            else:
                error = 3

            context = {
                "error": error,
                "rooms": rooms,
                "room": room,
                "meta_description": meta_description,
                "meta_keywords": "خانه معما , اتاق فرار , اسکیپ روم قم ," + room.name,
                "title": room.name,
                "now": now
            }
            return render(request, "main/reserveroom.html", context)
        if room.merchant == game_models.Room.RoomMerchant.PEC or request.user.is_authenticated:
            payment = PecMerchant().start_payment(**fields)
        else:
            payment = ZarinpalMerchant().start_payment(**fields)
        if payment.get("valid", None):
            return redirect(payment.get("url"))
        else:
            return redirect("main:room-page", slug=slug)


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
        img_alt = data.get('img-alt', "")
        is_archive = data.get('is_archive', False)
        is_archive = True if is_archive == 'on' else False
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
        admin_phones = data.get("admin_phones", None)
        if not admin_phones:
            admin_phones = functions.get_setting(enums.DefaultSettings.MAX_SMS_ADMIN_NUMBER)
        min_players = data.get("min_players", None)
        max_players = data.get("max_players", None)
        weekdays = data.getlist("weekday", None)
        hours = data.getlist("hours", None)
        hours.sort(key=lambda x: int(x.split(":")[0]))
        warnings = data.get("warnings", "")
        descriptions = data.get("descriptions", "")
        pre_pay = data.get("pre_pay", "")
        game_duration = data.get("duration", "")
        conditions = data.get("conditions", "")
        merchant = data.get("merchant",None)
        fields = {
            "name": name,
            "difficulty": difficulty,
            "price_per_unit": price,
            "default_hours": hours,
            "warnings": warnings,
            "pre_pay": pre_pay,
            "min_players": min_players,
            "max_players": max_players,
            "description": descriptions,
            "conditions": conditions,
            "admin_phones": admin_phones,
            "default_days": weekdays,
            "game_duration": game_duration,
            "google_map": data.get("google_map", ""),
            "balad_link": data.get("balad_link", ""),
            "room_type": this_type,
            "box_packages_prices": box_packages_prices,
            "is_archive": is_archive,
            "img_alt": img_alt,
            "merchant" : merchant
        }
        fields = functions.remove_empties(fields)
        room.update(**fields)
        room[0].banner = picture
        room[0].save()
        return redirect("main:rooms")

@method_decorator(csrf_exempt, name='dispatch')
class ReserveCompleted(View):

    def get(self, request):
        order_status = ZarinpalMerchant().verify_payment(request.GET.get("Authority"))
        return self.reserve(request=request,order_state=order_status)

    def post(self,request):
        token = request.POST.get("Token" , False)
        rrn = request.POST.get("RRN", 0)
        status = request.POST.get("status" , -1)
        try:
            rrn = int(rrn)
        except:
            pass
        try:
            status = int(status)
        except:
            pass
        if (status == 0 and rrn > 0):
            order_status = PecMerchant().verify_payment(authority=token)
        else:
            order_status = dict()
        response = self.reserve(request=request,order_status=order_status)
        return response


    def reserve(self,request,order_status):
        rooms = game_models.Room.objects.filter(room_type=enums.RoomType.REAL, is_archive=False)
        if order_status.get("ordered_before", False):
            now = datetime.datetime.now().strftime("%Y/%m/%d")
            room = order_status.get("room", None)
            redirect_url = reverse("main:room-page", kwargs={"slug": room.slug})
            parameters = urlencode({"error": 3})
            return redirect(f"{redirect_url}?{parameters}")
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


class TemplateSettingsView(LoginRequiredMixin, View):
    def get(self, request):
        return render(request, 'panel/template_settings.html', {"title": "تنظیمات قالب"})

    def post(self, request):
        data = request.POST.copy()
        data.pop("csrfmiddlewaretoken")
        for key, setting in data.items():
            name = key.lower()
            functions.set_context(name, setting)

        return redirect("main:template-settings")


class MangeUsersView(LoginRequiredMixin, ActionBaseView):
    model = User
    page_name = "کاربران"
    actions = ['create', 'delete', 'change_password']
    template_name = 'panel/users.html'

    def get(self, request):
        users = self.get_queryset().order_by('-date_joined')
        context = self.get_context_data({"title": self.page_name, "users": users})
        return render(request, self.template_name, context)
    

    def create(self, request):
        data = request.POST.dict()
        fields = ['first_name', 'last_name', 'username', 'password']

        
        

        if not all([bool(str(data.get(field, ""))) for field in fields]):
            messages.error(request, 'مقادیر ارسال شده متبر نیست')
            return redirect(reverse("main:users"))

        print("here")
        
        new_user = self.model(
            first_name=data.get('first_name'),
            last_name=data.get('last_name'),
            username=data.get('username'),
        )

        new_user.set_password(data.get('password'))
        new_user.save()
        return redirect(reverse("main:users"))
    

    def delete(self, request):
        pk = request.POST.get('pk', None)
        user = self.get_object(pk=pk)
        if user is None:
            messages.error(request, 'کاربر یافت نشد')
            return redirect(reverse("main:users"))
        
        user.delete()
        messages.success(request, 'کاربر با موفقیت حذف شد')
        return redirect(reverse("main:users"))
    

    def change_password(self, request):
        pk = request.POST.get('pk', 0)
        user = self.get_object(pk=pk)
        if user is None:
            messages.error(request, 'کاربر یافت نشد')
            return redirect(reverse("main:users"))
        
        password = request.POST.get('password', "")
        password1 = request.POST.get('password1', "")
        if not bool(str(password).strip()) or not bool(str(password1).strip()) or password != password1:
            messages.error(request, 'مقادیر ارسال شده متبر نیست')
            return redirect(reverse("main:users"))
        
        user.set_password(password)
        user.save()
        messages.success(request, 'رمز ورود کاربر تغییر کرد')
        return redirect(reverse("main:users"))