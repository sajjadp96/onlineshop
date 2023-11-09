from .models import Category,Product
from rest_framework.permissions import IsAuthenticated,IsAdminUser
from .serializers import CategorySerializer,ProductSerializer,IdSerialaizer
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import generics



class HelloView(APIView):
    
    def get(self, request):
        content = {'message': 'Hello'}
        return Response(content)




class CategoryList(APIView):
    
    def get(self, request):
        categorise = Category.objects.all()
        serializer = CategorySerializer(categorise, many=True)
        return Response(serializer.data)
    

class ProductList(APIView):
    
    # queryset = Product.objects.all()
    # serializer_class = ProductSerializer
    
    def get(self, request, format=None):
        products = Product.objects.all()
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)
    
    
    


class AddCategory(APIView):
    
    permission_classes = (IsAuthenticated,IsAdminUser,)
    
    def post(self,request):
        ser_data = CategorySerializer(data=request.data)
        if ser_data.is_valid():
            ser_data.save()
            return Response(ser_data.data, status=status.HTTP_201_CREATED)
        return Response(ser_data.errors, status=status.HTTP_400_BAD_REQUEST)
    
    
    def delete(self,request):
                
        ser_data = IdSerialaizer(data=request.data)
        
        if ser_data.is_valid():
            
            serialized_data = ser_data.data['ides']
            
            try:
                for i in serialized_data:
                    category = Category.objects.filter(id=i)
                    category.delete()
                    
            except Exception as e:
                return Response({'detail':f'error {str(e)}'})
            
        return Response({'message':'your order items deleted'})




class AddProductView(APIView):
    
    def post(self,request):
        ser_data = ProductSerializer(data=request.data)
        if ser_data.is_valid():
            ser_data.save()
            return Response(ser_data.data, status=status.HTTP_201_CREATED)
        return Response(ser_data.errors, status=status.HTTP_400_BAD_REQUEST)
    

    
    def delete(self,request):
                        
        ser_data = IdSerialaizer(data=request.data)
        
        if ser_data.is_valid():
            
            serialized_data = ser_data.data['ides']
            
            try:
                for i in serialized_data:
                    product = Product.objects.filter(id=i)
                    product.delete()
                    
            except Exception as e:
                return Response({'detail':f'error {str(e)}'})
            
        return Response({'message':'your order items deleted'})



class SearchView(APIView):
    
    def get(self, request):
        searched = request.GET.get('searched')
        FOODS_QUERYSET = Product.objects.filter(name__contains=searched).distinct()
        serializer = ProductSerializer(FOODS_QUERYSET,many=True)
        return Response(serializer.data)
    

class CategoryDetailView(APIView):
    
    def get(self,request,pk):
        category = Category.objects.get(id=pk)
        serializer = CategorySerializer(category)
        return Response(serializer.data)
        

class UpdateCategroryView(APIView):
       
    permission_classes = (IsAuthenticated,IsAdminUser)
    
    def put(self,request):
        pass 
        

class ProductDetailView(APIView):
    
    
    def get(self,request,pk):
        product=Product.objects.get(id=pk)
        serializer = ProductSerializer(product)
        return Response(serializer.data)
    
    

class UpdateProductView(APIView):
    
    permission_classes = (IsAuthenticated,IsAdminUser)
    

    def put(self,request):
        pass