from django.db import models
from riddlehouse.helpers import enums


class Order(models.Model):
    room = models.ForeignKey("game.Room", on_delete=models.DO_NOTHING)
    customer_name = models.CharField(max_length=255)
    customer_number = models.CharField(max_length=15)
    transaction_number = models.CharField(max_length=255)
    players_number = models.IntegerField()
    pre_payment = models.IntegerField()
    key = models.CharField(max_length=4)
    rest_payment = models.IntegerField()
    used_coupon = models.CharField(max_length=15, null=True, blank=True)
    payment_time = models.DateTimeField(auto_now_add=True)
    sms_bulk = models.CharField(null=True, blank=True)
    reserved_time = models.DateTimeField()


class Coupon(models.Model):
    available_rooms = models.ManyToManyField("game.Room", related_name="coupons")
    type = models.CharField(max_length=1, choices=enums.CouponsType.choices, default=enums.CouponsType.PERCENTAGE)
    amount = models.IntegerField()
    used = models.IntegerField(null=True, blank=True)
    capacity = models.IntegerField()
