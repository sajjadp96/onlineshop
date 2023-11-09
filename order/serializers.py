from rest_framework import serializers
from .models import Order,OrderItem
from rest_framework.response import Response
from user.serializers import Profileserializer,AddressSerializer
from user.models import User


class OrderItemSerializer(serializers.ModelSerializer):
    
    product = serializers.SlugRelatedField(read_only=True,slug_field='name')
    class Meta:
        model = OrderItem
        fields = ['id',"product","quantity","discount","price",]
        
        

class OrderSerializer(serializers.ModelSerializer):
    
    price = serializers.SerializerMethodField()
    items = OrderItemSerializer(many=True,read_only=True)
    address = serializers.StringRelatedField()
    

    def get_price(self, obj):
        return obj.final_price
    class Meta:
        model = Order
        fields = ['id','status','address','created_at',"discount",'price','items',"discount"]
        # fields = ['order','product','quantity','price']


class PrudoctSerializer(serializers.Serializer):
    
    orders = serializers.DictField() 
    
    def validate(self,data):
        for i,j in data['orders'].items():
            if i.isdigit() and j.isdigit():
                return data
            
        return Response({"detail":"data must be digit."})
    
    
class OrederIdSerialaizer(serializers.Serializer):
    
    ides= serializers.ListField()
    
    def validate(self,data):
        
        for i in data['ides']:
            if not isinstance(i,int):
                return Response({"detail":"data must be digit."})
                
        return data
            
    
    