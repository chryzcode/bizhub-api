from rest_framework import serializers
from .models import *


ORDER_TYPE_CHOICES = (
    ("SERVICES", "SERVICES"),
    ("SALES", "SALES")
)



class CreateOrderSerializer(serializers.Serializer):
    due_date = serializers.DateField()
    description = serializers.CharField()
    order_type = serializers.ChoiceField(ORDER_TYPE_CHOICES)
    amount = serializers.IntegerField()

class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = '__all__'
