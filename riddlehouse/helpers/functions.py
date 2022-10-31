from main import models as main_models
from game import models as game_models
from orders import models as orders_models
from django.core import exceptions
from . import enums
import requests
import json
import random


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
    amount = int(kwargs.get("amount", 10000))
    if not merchant or not amount:
        return False
    zarinpal_url = get_setting(enums.DefaultSettings.ZARINPAL_START_URL)
    callback_url = get_setting(enums.DefaultSettings.ZARINPAL_CALLBACK_URL)

    description = kwargs.get("description", "پرداخت خانه معما")
    data = {
        "merchant_id": merchant,
        "amount": 10000,
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
            return {"valid": True, "data": response['data']}
        else:
            return {"valid": False, "data": "Failed to create payment object"}
    pass


def create_payment_object(**kwargs):
    try:
        room = game_models.Room.objects.get(pk=kwargs['room_id'])
    except exceptions.ObjectDoesNotExist as e:
        print(e)
        return None

    fields = {
        "room": room,
        "customer_name": kwargs.get('customer_name', None),
        "customer_number": kwargs.get('mobile', None),
        "authority_key": kwargs.get('authority', None),
        "players_number": kwargs.get('players_number', None),
        "amount": kwargs.get('amount', None),
        "used_coupon": kwargs.get('coupon', None),
        "reserved_time": kwargs.get('reserved_time', None),
    }
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
    amount = payment.amount
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

    pass


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
    rest_payment = int(payment.room.final_payment) - int(payment.amount)
    fields = {
        "room": payment.room,
        "card_pan": card_pan,
        "rest_payment": rest_payment,
        "customer_name": payment.customer_name,
        "transaction_number": transaction_number,
        "players_number": payment.players_number,
        "paid": payment.amount,
        "key": key,
        "used_coupon": payment.used_coupon,
        "reserved_time": payment.reserved_time
    }
    order = orders_models.Order(**fields)
    order.save()
    send_sms(order)
    return order


def send_sms(order):
    try:
        admin_sms = send_admin_sms(order)
        print(admin_sms)
    except Exception as e:
        print(e)
    try:
        user_sms = send_user_sms(order)
        print(user_sms)
    except Exception as e:
        print(e)
    return


def send_admin_sms(order):
    to_number = get_setting(enums.DefaultSettings.MAX_SMS_ADMIN_NUMBER)
    input_data = {
        "user": order.customer_name,
        "phone": order.customer_number,
        "game": order.room.name,
        "pers": order.players_number,
        "date": order.reserved_time.date(),
        "time": order.reserved_time.time(),
        "key": order.key,
        "transid": order.transaction_number
    }
    url, data = get_sms_configs("admin", to_number, input_data)
    if not url:
        return False
    request = requests.post(url, data=data)
    response = json.loads(request.text)
    return response


def send_user_sms(order: orders_models.Order):
    to_number = order.customer_number
    input_data = {
        "user": order.customer_name,
        "game": order.room.name,
        "date": order.reserved_time.date(),
        "time": order.reserved_time.time(),
        "key": order.key
    }
    url, data = get_sms_configs("user", to_number, input_data)
    if not url:
        return False
    request = requests.post(url, data=data)
    response = json.loads(request.text)
    return response


def get_sms_configs(receiver: str, to_number, input_data):
    url = get_setting(enums.DefaultSettings.MAX_SMS_API_URL)
    username = get_setting(enums.DefaultSettings.MAX_SMS_USERNAME)
    password = get_setting(enums.DefaultSettings.MAX_SMS_PASSWORD)
    from_number = get_setting(enums.DefaultSettings.MAX_SMS_LINE_NUMBER)
    if receiver == "user":
        pattern = get_setting(enums.DefaultSettings.MAX_SMS_USER_PATTERN_CODE)
    elif receiver == "admin":
        pattern = get_setting(enums.DefaultSettings.MAX_SMS_ADMIN_PATTERN_CODE)
    else:
        return False, False
    data = {
        "op": "pattern",
        "user": username,
        "pass": password,
        "fromNum": from_number,
        "toNum": to_number,
        "patternCode": pattern,
        "inputData": input_data,
    }
    return url, data


def set_setting(name , value):
    setting_object = main_models.Setting.objects.filter(name=name)
    setting = enums.DefaultSettings[name]
    if setting_object.exists():
        setting_object.update(value=value)
    else:
        setting_object = main_models.Setting(slug=setting.value['slug'],value=value,name=name)
        setting_object.save()