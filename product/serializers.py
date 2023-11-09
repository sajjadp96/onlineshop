from rest_framework import serializers
from .models import Category,Product
from rest_framework.response import Response


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'title', 'description', 'image', 'category']
        
        

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id','name','description','image','price','category','status']
        

class IdSerialaizer(serializers.Serializer):
    
    ides= serializers.ListField()
    
    def validate(self,data):
        
        for i in data['ides']:
            if not isinstance(i,int):
                return Response({"detail":"data must be digit."})
                
        return data