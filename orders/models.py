from django.db import models
from riddlehouse.helpers import enums


class Order(models.Model):
    room = models.ForeignKey("game.Room", on_delete=models.DO_NOTHING, related_name="orders")
    customer_name = models.CharField(max_length=255)
    customer_number = models.CharField(max_length=15)
    transaction_number = models.CharField(max_length=255)
    players_number = models.IntegerField()
    paid = models.IntegerField()
    key = models.CharField(max_length=4)
    rest_payment = models.IntegerField()
    used_coupon = models.CharField(max_length=15, null=True, blank=True)
    user_sms_bulk = models.CharField(max_length=31, null=True, blank=True)
    admin_sms_bulk = models.CharField(max_length=31, null=True, blank=True)
    card_pan = models.CharField(max_length=127,null=True,blank=True)
    reserved_time = models.DateTimeField()
    created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.customer_name} - ({self.room} : {self.reserved_time})"


class Coupon(models.Model):
    available_rooms = models.ManyToManyField("game.Room", related_name="coupons")
    type = models.CharField(max_length=1, choices=enums.CouponsType.choices, default=enums.CouponsType.PERCENTAGE)
    amount = models.IntegerField()
    used = models.IntegerField(null=True, blank=True)
    capacity = models.IntegerField()


class Payment(models.Model):
    room = models.ForeignKey("game.Room", on_delete=models.DO_NOTHING, related_name="payments")
    is_completed = models.BooleanField(default=False)
    customer_name = models.CharField(max_length=255)
    customer_mobile = models.CharField(max_length=15)
    authority_key = models.CharField(max_length=255)
    players_number = models.IntegerField()
    amount = models.IntegerField()
    used_coupon = models.CharField(max_length=15, null=True, blank=True)
    reserved_time = models.DateTimeField()
    created_date = models.DateTimeField(auto_now_add=True)
