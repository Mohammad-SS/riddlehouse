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
    REAL = "REAL", "اتاق عادی"
    BOX = "BOX", "اسکیپ باکس"


class RoomPaymentMethod(models.TextChoices):
    PER_PERSON = "P", "Per Person"
    TOTAL = "T", "Total"


class CouponsType(models.TextChoices):
    PERCENTAGE = "P", "percent"
    CONSTANT = "C", "const"


class RuleTypes(models.TextChoices):
    SINGLE_DAY = "D", "Single Day"
    WEEK_DAY = "W", "Week Day"


class DefaultSettings(Enum):
    LIMIT_DAYS_FOR_RESERVATION = {"slug": "limits_day_reservation", "default": 30}
    ZARINPAL_MERCHANT_KEY = {"slug": "zarinpal_merchant", "default": None}
    LOCATION_ADDRESS = {"slug": "location_address", "default": ""}
    ABOUT_US = {"slug": "about_us", "default": ""}
    MOBILE_PHONE = {"slug": "mobile_phone", "default": ""}
    EMAIL_ADDRESS = {"slug": "email_address", "default": ""}
    TELEGRAM_ID = {"slug": "telegram_id", "default": ""}
    INSTAGRAM_USER = {"slug": "instagram_user", "default": ""}
    WHATSAPP_NUMBER = {"slug": "whatsapp_number", "default": ""}
    MAX_SMS_API_URL = {"slug": "max_sms_api_url", "default": "https://ippanel.com/patterns/pattern"}
    MAX_SMS_ADMIN_PATTERN_CODE = {"slug": "max_sms_admin_pattern_code", "default": "0syz2av5yv"}
    MAX_SMS_USER_PATTERN_CODE = {"slug": "max_sms_user_pattern_code", "default": "lqtobvthhs"}
    MAX_SMS_USERNAME = {"slug": "max_sms_username", "default": False}
    MAX_SMS_PASSWORD = {"slug": "max_sms_password", "default": False}
    MAX_SMS_LINE_NUMBER = {"slug": "max_sms_line_number", "default": "5000125475"}
    MAX_SMS_ADMIN_NUMBER = {"slug": "max_sms_admin_number", "default": "09212518775,09358051274"}
    MAX_SMS_SURPRISE_USER_PATTERN_CODE = {"slug": "max_sms_surprise_user_pattern_code", "default": "gy6ikksu5t"}
    ZARINPAL_PAYMENT_URL = {"slug": "zarinpal_payment_url", "default": "https://www.zarinpal.com/pg/StartPay/"}
    ZARINPAL_START_URL = {"slug": "zarinpal_start_url",
                          "default": "https://api.zarinpal.com/pg/v4/payment/request.json"}
    ZARINPAL_VERIFY_URL = {"slug": "zarinpal_verify_url",
                           "default": "https://api.zarinpal.com/pg/v4/payment/verify.json"}
    ZARINPAL_CALLBACK_URL = {"slug": "zarinpal_callback", "default": "http://127.0.0.1:8000" + "/reserve-completed"}


class ExclusionsType(models.TextChoices):
    DATE = "D" , "بر اساس تاریخ"
    DATE_AND_WEEKDAY = "DW" , "بر اساس روز هفته و تاریخ"
