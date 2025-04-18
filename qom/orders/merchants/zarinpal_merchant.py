import requests
from game import models as game_models
from orders import models as orders_models
from riddlehouse.helpers import enums
from riddlehouse.helpers.functions import get_setting, validate_coupon, get_amount_after_coupon, \
    create_random_authority, create_payment_object, place_order, send_sms
from .base_merchant import BaseMerchant


class ZarinpalMerchant(BaseMerchant):

    def start_payment(self, **kwargs):
        merchant = get_setting(enums.DefaultSettings.ZARINPAL_MERCHANT_KEY, "cd7b446a-17d3-11e9-ab83-005056a205be")
        zarinpal_url = get_setting(enums.DefaultSettings.ZARINPAL_START_URL)
        callback_url = get_setting(enums.DefaultSettings.ZARINPAL_CALLBACK_URL)
        zarinpal_payment_url = get_setting(enums.DefaultSettings.ZARINPAL_PAYMENT_URL)
        amount = kwargs.get("amount", None)
        if not merchant or not amount:
            return False
        coupon = kwargs.get("coupon", None)

        room_id = kwargs.get("room_id", None)
        room = game_models.Room.objects.get(pk=room_id)
        coupon = orders_models.Coupon.objects.filter(code=coupon)
        amount = int(amount)
        if coupon.exists():
            coupon = coupon[0]
        else:
            coupon = None

        if validate_coupon(room, coupon):
            coupon.used += 1
            coupon.save()
            amount = get_amount_after_coupon(coupon, amount)

        kwargs['amount'] = amount
        if amount == 0:
            kwargs['authority'] = create_random_authority()
            payment_obj = create_payment_object(**kwargs)
            return {"valid": True,
                    "url": callback_url + "?Authority=" + kwargs['authority'] + "&Status=" + "OK"}
        description = f"پرداخت به نام {kwargs.get('customer_name', '')} با شماره تلفن  {kwargs.get('mobile', '')}"
        data = {
            "merchant_id": merchant,
            "amount": amount * 10,
            "callback_url": callback_url,
            "description": description,
        }
        request_obj = requests.post(zarinpal_url, data=data)
        response = request_obj.json()
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

    def verify_payment(self, authority):
        merchant = get_setting(enums.DefaultSettings.ZARINPAL_MERCHANT_KEY, "cd7b446a-17d3-11e9-ab83-005056a205be")
        try:
            payment = orders_models.Payment.objects.get(authority_key=authority)
        except orders_models.Payment.DoesNotExist as e:
            print(e)
            return {"valid": False, "data": "No Authority key found", "payment": None, "order": None}
        # ordered_before = orders_models.Order.objects.filter(reserved_time=payment.reserved_time, room=payment.room)
        ordered_before = orders_models.Order.objects.filter(reserved_time=payment.reserved_time,
                                                            room=payment.room).exclude(
            customer_number=payment.customer_mobile)

        if ordered_before.exists():
            return {"valid": False, "ordered_before": True, "room": payment.room}
        amount = payment.amount * 10
        if amount == 0:
            order_object, payment_object = place_order(authority, "رایگان - " + authority[0:15], "بدون پرداخت")
            if not order_object.user_sms_bulk or not order_object.admin_sms_bulk:
                send_sms.delay(order=order_object.pk)
            data = {
                "code": 200,
                "ref_id": "رایگان",
                "card_pan": "ندارد",
                "card_hash": "رایگان",
            }
            return {"valid": True, "data": data, "order": order_object, "payment": payment_object}
        url = get_setting(enums.DefaultSettings.ZARINPAL_VERIFY_URL)
        data = {
            "merchant_id": merchant,
            "amount": amount,
            "authority": authority
        }
        request = requests.post(url, data=data)
        response = request.json()

        if response['errors']:
            return {"valid": False, "data": response['errors'], "payment": payment, "order": None}
        else:
            order_object, payment_object = place_order(authority, response['data']['ref_id'],
                                                       response['data']['card_pan'])
            if order_object:
                if not order_object.user_sms_bulk or not order_object.admin_sms_bulk:
                    send_sms.delay(order=order_object.pk)
                return {"valid": True, "data": response['data'], "order": order_object, "payment": payment_object}
            else:
                return {"valid": False, "data": "Failed to place order", "payment": None, "order": None}
