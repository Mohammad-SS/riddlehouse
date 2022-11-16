from celery import shared_task
from .helpers.functions import send_admin_sms , send_user_sms

@shared_task
def send_sms(order):
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