from main import models as main_models
from game import models as game_models
from orders import models as orders_models
from django.core import exceptions
from . import enums
import requests
import json
import random
from persiantools import jdatetime


def get_setting(setting, default=None):
    setting_slug = setting.value.get("slug", None)
    if not setting_slug:
        return default

    setting_default = setting.value.get("default", None)
    if not setting_default:
        setting_default = default
    try:
        return main_models.Setting.objects.get(slug=setting_slug).value
    except exceptions.ObjectDoesNotExist:
        return setting_default


def start_payment(**kwargs):
    merchant = get_setting(enums.DefaultSettings.ZARINPAL_MERCHANT_KEY, "cd7b446a-17d3-11e9-ab83-005056a205be")
    amount = kwargs.get("amount", None)
    if not merchant or not amount:
        return False
    amount = int(amount)
    zarinpal_url = get_setting(enums.DefaultSettings.ZARINPAL_START_URL)
    callback_url = get_setting(enums.DefaultSettings.ZARINPAL_CALLBACK_URL)
    zarinpal_payment_url = get_setting(enums.DefaultSettings.ZARINPAL_PAYMENT_URL)

    description = kwargs.get("description", "پرداخت خانه معما")
    data = {
        "merchant_id": merchant,
        # "amount": amount * 10,
        "amount": 1000,
        "callback_url": callback_url,
        "description": description,
    }
    request_obj = requests.post(zarinpal_url, data=data)
    response = json.loads(request_obj.text)
    if response['errors']:
        return {"valid": False, "data": response['errors']}
    else:
        kwargs['authority'] = response['data']['authority']
        payment_obj = create_payment_object(**kwargs)
        if payment_obj:
            return {"valid": True, "data": response['data'],
                    "url": zarinpal_payment_url + response['data']['authority']}
        else:
            return {"valid": False, "data": "Failed to create payment object"}


def create_payment_object(**kwargs):
    try:
        room = game_models.Room.objects.get(pk=kwargs['room_id'])
    except exceptions.ObjectDoesNotExist as e:
        print(e)
        return None
    package = kwargs.get("package", None)
    if not package or package == "":
        package = None
    fields = {
        "room": room,
        "customer_name": kwargs.get('customer_name', None),
        "customer_mobile": kwargs.get('mobile', None),
        "authority_key": kwargs.get('authority', None),
        "players_number": kwargs.get('players_number', None),
        "package": package,
        "amount": kwargs.get('amount', None),
        "used_coupon": kwargs.get('coupon', None),
        "reserved_time": kwargs.get('reserved_time', None),
    }
    print(fields)
    obj = orders_models.Payment(**fields)
    obj.save()
    return obj


def verify_payment(authority):
    merchant = get_setting(enums.DefaultSettings.ZARINPAL_MERCHANT_KEY, "cd7b446a-17d3-11e9-ab83-005056a205be")
    try:
        payment = orders_models.Payment.objects.get(authority_key=authority)
    except exceptions.ObjectDoesNotExist as e:
        print(e)
        return False
    # amount = payment.amount * 10
    amount = 1000
    url = get_setting(enums.DefaultSettings.ZARINPAL_VERIFY_URL)
    data = {
        "merchant_id": merchant,
        "amount": amount,
        "authority": authority
    }
    request = requests.post(url, data=data)
    response = json.loads(request.text)
    if response['errors']:
        return {"valid": False, "data": response['errors']}
    else:
        order_object = place_order(authority, response['data']['ref_id'], response['data']['card_pan'])
        if order_object:
            send_sms(order_object)
            return {"valid": True, "data": response['data'], "order": order_object}
        else:
            return {"valid": False, "data": "Failed to place order"}


def place_order(authority, transaction_number=None, card_pan=None):
    """
    finds payment with authority and create order object
    """
    try:
        payment = orders_models.Payment.objects.get(authority_key=authority)
    except exceptions.ObjectDoesNotExist as e:
        print(e)
        return False
    key = random.randint(1000, 9999)
    fields = {
        "room": payment.room,
        "card_pan": card_pan,
        "customer_name": payment.customer_name,
        "customer_number": payment.customer_mobile,
        "transaction_number": transaction_number,
        "players_number": payment.players_number,
        "paid": payment.amount,
        "key": key,
        "package": payment.package,
        "used_coupon": payment.used_coupon,
        "reserved_time": payment.reserved_time
    }

    order , created = orders_models.Order.objects.get_or_create(transaction_number=transaction_number , defaults=fields)
    payment.is_completed = True
    payment.save()
    send_sms(order)
    return order


def send_sms(order : orders_models.Order):
    try:
        admin_sms = send_admin_sms(order)
        order.admin_sms_bulk = admin_sms
        order.save()
    except Exception as e:
        print(e)
    try:
        user_sms = send_user_sms(order)
        order.user_sms_bulk = user_sms
        order.save()
    except Exception as e:
        print(e)


def send_admin_sms(order):
    to_number = get_setting(enums.DefaultSettings.MAX_SMS_ADMIN_NUMBER)
    if order.room.room_type == enums.RoomType.BOX:
        persons = "ندارد"
        time = "-"
    else:
        persons = order.players_number
        time = order.reserved_time.time().strftime("%-H:%-M")
    date = jdatetime.JalaliDateTime.fromtimestamp(order.reserved_time.timestamp()).replace(locale="fa").strftime(
        "%A %Y/%m/%d")
    input_data = {
        "user": order.customer_name,
        "phone": order.customer_number,
        "game": order.room.name,
        "pers": persons,
        "date": date,
        "time": time,
        "key": order.key,
        "transid": order.transaction_number
    }
    url, data = get_sms_configs("admin", to_number, input_data)
    if not url:
        return False
    request = requests.get(url, data)
    response = json.loads(request.text)

    return response


def get_surprise_input_date(order: orders_models.Order):
    date = jdatetime.JalaliDateTime.fromtimestamp(order.reserved_time.timestamp()).replace(locale="fa").strftime(
        "%A %Y/%m/%d")

    input_data = {
        "user": order.customer_name,
        "date": date,
        "key": order.key
    }
    return input_data


def get_room_input_data(order):
    date = jdatetime.JalaliDateTime.fromtimestamp(order.reserved_time.timestamp()).replace(locale="fa").strftime(
        "%A %Y/%m/%d")
    time = order.reserved_time.time().strftime("%-H:%-M")
    input_data = {
        "user": order.customer_name,
        "game": order.room.name,
        "date": date,
        "time": time,
        "key": order.key,
    }
    return input_data


def send_user_sms(order: orders_models.Order):
    to_number = order.customer_number
    if order.room.room_type == enums.RoomType.BOX:
        input_data = get_surprise_input_date(order)
    else:
        input_data = get_room_input_data(order)

    url, data = get_sms_configs("user", to_number, input_data, surprise=True)

    if not url:
        return False
    request = requests.get(url, data)
    response = json.loads(request.text)
    return response


def get_sms_configs(receiver: str, to_number, input_data, surprise=False):
    url = get_setting(enums.DefaultSettings.MAX_SMS_API_URL)
    username = get_setting(enums.DefaultSettings.MAX_SMS_USERNAME)
    password = get_setting(enums.DefaultSettings.MAX_SMS_PASSWORD)
    from_number = get_setting(enums.DefaultSettings.MAX_SMS_LINE_NUMBER)
    if receiver == "user":
        if surprise:
            pattern = get_setting(enums.DefaultSettings.MAX_SMS_SURPRISE_USER_PATTERN_CODE)
        else:
            pattern = get_setting(enums.DefaultSettings.MAX_SMS_USER_PATTERN_CODE)
    elif receiver == "admin":
        pattern = get_setting(enums.DefaultSettings.MAX_SMS_ADMIN_PATTERN_CODE)
    else:
        return False, False
    data = {
        "username": username,
        "password": password,
        "from": from_number,
        "to": to_number,
        "input_data": json.dumps(input_data),
        "pattern_code": pattern
    }
    return url, data


def set_setting(name, value):
    setting_object = main_models.Setting.objects.filter(name=name)
    setting = enums.DefaultSettings[name]
    if setting_object.exists():
        setting_object.update(value=value)
    else:
        setting_object = main_models.Setting(slug=setting.value['slug'], value=value, name=name)
        setting_object.save()
