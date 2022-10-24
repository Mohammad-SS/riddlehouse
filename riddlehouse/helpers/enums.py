from django.db import models
from enum import Enum
from riddlehouse import settings


class WeekDays(models.IntegerChoices):
    SATURDAY = 1, "شنبه"
    SUNDAY = 2, "یک شنبه"
    MONDAY = 3, "دو شنبه"
    TUESDAY = 4, "سه شنبه"
    WENDSAY = 5, "چهار شنبه"
    THURSDAY = 6, "پنج شنبه"
    FRIDAY = 7, "جمعه"

class RoomType(models.TextChoices):
    REAL = "REAL" , "اتاق عادی"
    BOX = "BOX" , "اسکیپ باکس"


class RoomPaymentMethod(models.TextChoices):
    PER_PERSON = "P", "Per Person"
    TOTAL = "T", "Total"


class CouponsType(models.TextChoices):
    PERCENTAGE = "P", "%"
    CONSTANT = "C", "Const"


class RuleTypes(models.TextChoices):
    SINGLE_DAY = "D", "Single Day"
    WEEK_DAY = "W", "Week Day"


class DefaultSettings(Enum):
    LIMIT_DAYS_FOR_RESERVATION = {"slug": "limits_day_reservation", "default": 30}
    ZARINPAL_MERCHANT_KEY = {"slug": "zarinpal_merchant", "default": None}
    MAX_SMS_API_URL = {"slug": "max_sms_api_url", "default": "http://ippanel.com/api/select"}
    MAX_SMS_ADMIN_PATTERN_CODE = {"slug": "max_sms_admin_pattern_code", "default": "0syz2av5yv"}
    MAX_SMS_USER_PATTERN_CODE = {"slug": "max_sms_user_pattern_code", "default": "lqtobvthhs"}
    MAX_SMS_USERNAME = {"slug": "max_sms_username", "default": False}
    MAX_SMS_PASSWORD = {"slug": "max_sms_password", "default": False}
    MAX_SMS_LINE_NUMBER = {"slug": "max_sms_line_number", "default": "100020400"}
    MAX_SMS_ADMIN_NUMBER = {"slug": "max_sms_admin_number", "default": "09212518775"}
    MAX_SMS_SURPRISE_USER_PATTERN_CODE = {"slug": "max_sms_surprise_user_pattern_code", "default": "gy6ikksu5t"}
    ZARINPAL_START_URL = {"slug": "zarinpal_start_url",
                          "default": "https://api.zarinpal.com/pg/v4/payment/request.json"}
    ZARINPAL_VERIFY_URL = {"slug": "zarinpal_verify_url",
                           "default": "https://api.zarinpal.com/pg/v4/payment/verify.json"}
    ZARINPAL_CALLBACK_URL = {"slug": "zarinpal_callback", "default": "http://127.0.0.1:8000" + "/reserve-completed"}
