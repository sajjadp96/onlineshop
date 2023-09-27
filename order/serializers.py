from rest_framework import serializers
from .models import Order,OrderItem


class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = ['customer', 'address',]
        
        

class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ['order','product','quantity','price']