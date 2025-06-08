from .base_merchant import BaseMerchant
import requests
from game import models as game_models
from orders import models as orders_models
from riddlehouse.helpers import enums
from riddlehouse.helpers.functions import get_setting, validate_coupon, get_amount_after_coupon, \
    create_random_authority, create_payment_object, place_order, send_sms
from zeep import Client
from zeep.exceptions import Fault

class PecMerchant(BaseMerchant):

    def __init__(self):
        self.pin = "336HOyi0G55xEI38S2CJ"
        self.call_back = "https://qom.riddlehouse.ir/reserve-completed"


    def start_payment(self, **kwargs):
        amount = kwargs.get("amount", None)
        if not amount:
            return False
        coupon = kwargs.get("coupon", None)
        room_id = kwargs.get("room_id", None)
        room = game_models.Room.objects.get(pk=room_id)
        coupon = orders_models.Coupon.objects.filter(code=coupon)
        amount = int(amount) * 10
        if coupon.exists():
            coupon = coupon[0]
        else:
            coupon = None

        if validate_coupon(room, coupon):
            coupon.used += 1
            coupon.save()
            amount = get_amount_after_coupon(coupon, amount,unit="RIAL")

        kwargs['amount'] = amount
        if amount == 0:
            kwargs['authority'] = create_random_authority()
            payment_obj = create_payment_object(**kwargs)
            return {"valid": True,
                    "url": self.call_back + "?Authority=" + kwargs['authority'] + "&Status=" + "OK"}
        description = f"پرداخت به نام {kwargs.get('customer_name', '')} با شماره تلفن  {kwargs.get('mobile', '')}"
        wsdl_url = "https://pec.shaparak.ir/NewIPGServices/Sale/SaleService.asmx?WSDL"
        kwargs["authority"] = "TEMP_PEC"
        payment_obj = create_payment_object(**kwargs)
        params = {
            "LoginAccount": self.pin,
            "Amount": int(amount),
            "OrderId": payment_obj.id,
            "CallBackUrl": self.call_back,
        }
        print(params,"***********************************************************")
        client = Client(wsdl=wsdl_url)
        result = client.service.SalePaymentRequest(requestData=params)
        if result.Token and result.Status == 0:
            payment_url = f"https://pec.shaparak.ir/NewIPG/?Token={result.Token}"
            kwargs['authority'] = result.Token
            if payment_obj:
                payment_obj.authority_key = result.Token
                payment_obj.save()
                return {"valid": True, "url": f"https://pec.shaparak.ir/NewIPG/?Token={result.Token}"}
            else:
                return {"valid": False, "data": "Failed to create payment object"}
        else:
            return {"valid": False, "data": result.Message}

    def verify_payment(self, authority):
        merchant = get_setting(enums.DefaultSettings.ZARINPAL_MERCHANT_KEY, "cd7b446a-17d3-11e9-ab83-005056a205be")
        try:
            payment = orders_models.Payment.objects.get(authority_key=authority)
        except orders_models.Payment.DoesNotExist as e:
            print(e)
            return {"valid": False, "data": "No Authority key found", "payment": None, "order": None}
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



        wsdl_url = 'https://pec.shaparak.ir/NewIPGServices/Confirm/ConfirmService.asmx?WSDL'
        params = {
            "LoginAccount": self.pin,
            "Token": authority
        }
        client = Client(wsdl=wsdl_url)
        result = client.service.ConfirmPayment(requestData=params)
        if result.Status != 0:
            return {"valid": False, "data": result.Status, "payment": payment, "order": None}
        else:
            order_object, payment_object = place_order(authority,authority,authority)
            if order_object:
                if not order_object.user_sms_bulk or not order_object.admin_sms_bulk:
                    send_sms.delay(order=order_object.pk)
                return {"valid": True, "data": authority, "order": order_object, "payment": payment_object}
            else:
                return {"valid": False, "data": "Failed to place order", "payment": None, "order": None}
