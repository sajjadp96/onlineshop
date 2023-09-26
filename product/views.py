from .models import Category,Product
from .serializers import CategorySerializer,ProductSerializer
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

class CategoryList(APIView):
    """
    List all Category.
    """
    def get(self, request, format=None):
        categorise = Category.objects.all()
        serializer = CategorySerializer(categorise, many=True)
        return Response(serializer.data)

class ProductList(APIView):
    """
    List all Category.
    """
    def get(self, request, format=None):
        products = Product.objects.all()
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)