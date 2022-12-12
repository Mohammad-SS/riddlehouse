from rest_framework import serializers
from orders import models as order_models
from game import models as game_models


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = order_models.Order
        fields = "__all__"


class GameSerializer(serializers.ModelSerializer):
    class Meta:
        model = game_models.Room
        fields = "__all__"
