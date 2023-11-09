from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated,IsAdminUser
from .serializers import PrudoctSerializer,OrderItemSerializer,OrderSerializer,OrederIdSerialaizer
from .models import Order,OrderItem
from rest_framework.response import Response
from user.models import Address
from rest_framework import status
from django.db import transaction
from product.models import Product
from user.models import User
from user.tasks import send_notification_mail
from django.core.exceptions import ObjectDoesNotExist
# from user.utils import get_all_users_email,ad_message



class AddOrderView(APIView):
    
    permission_classes =(IsAuthenticated,)
    
    def post(self,request):
        
        user = request.user
        ser_data = PrudoctSerializer(data=request.data)
        try:
            address = Address.objects.get(user=user)
        except ObjectDoesNotExist:
            return Response({"detial":"add address first."},status=status.HTTP_400_BAD_REQUEST)
        order = Order(customer=user,address = address)
        
        if ser_data.is_valid():
            
            serialized_data = ser_data.data['orders']
            
            with transaction.atomic():
                order.save()
            
                for product_id,quantity in serialized_data.items(): 
                    product = Product.objects.get(id=product_id)
                    orderitem = OrderItem(
                        order = order,
                        product = product,
                        quantity = int(quantity),
                        price = product.price,
                        discount = product.discount
                    )
                    orderitem.save()
                    
            return Response({"message":"your order is confirmed"})
        
        return Response({"detail":"somethings went wrong."})

    
    def delete(self,request,pk):
        
        user = request.user
        
        try:
            order = Order.objects.filter(id=pk,status="Pending",customer=user.id)
            if len(order) == 0:
                return Response({"detail":"order is not found"})
            order.delete()
        except Exception as e:
            return Response({'detail':f"this error happend {str(e)}"})
        
        return Response({'massage':'your order deleted.'})



class OrdersView(APIView):
    
    permission_classes =(IsAuthenticated,)
    
    def get(self,request):
        
        user = request.user
        
        try:
            order = Order.objects.filter(customer=user.id)
            serializer = OrderSerializer(order,many=True)
                        
        except Exception as e :
              return Response({"detail":f"somethings went wrong. {str(e)}"})
        
        return Response(serializer.data) 
        
        
class OrderDetailsView(APIView):
    
    # permission_classes = (IsAuthenticated,)
    
    def get(self,request,pk):
        
        user = request.user
        
        try:
            orderitem = OrderItem.objects.filter(id=pk,order__customer_id=user.id)
            ser_data =OrderItemSerializer(orderitem,many=True)
        
        except Exception as e:
            return Response({'detail':f'Error {str(e)}'})
        
        return Response(ser_data.data)
    
    
    
    def put(self,request,pk):
        
        ser_data = PrudoctSerializer(data=request.data)
        
        user = request.user
        
        if ser_data.is_valid():
            
            serialized_data = ser_data.data['orders']
            
            try:
                
                orderitem = OrderItem.objects.filter(order_id=pk,order__customer_id=user.id)
                 
                for key,value in serialized_data.items():
                    
                    if  len(order_i := orderitem.filter(product=key))>0:
                        order_i.update(quantity=value)
                        
                    else:
                        product = Product.objects.get(id=key)
                        orderitem.create(order_id=pk,product=product,quantity=value,price=product.price,discount=product.discount)

            except Exception as e:
                return Response({'detail':f'error {str(e)}'})
        return Response({'message':'your order items updated'})
    
    
    
    def delete(self,request):
        
        user = request.user
        
        ser_data = OrederIdSerialaizer(data=request.data)
        
        if ser_data.is_valid():
            
            serialized_data = ser_data.data['ides']
            
            try:
                for i in serialized_data:
                    orderitem = OrderItem.objects.filter(id=i,order__customer_id=user.id)
                    orderitem.delete()
                    
            except Exception as e:
                return Response({'detail':f'error {str(e)}'})
            
        return Response({'message':'your order items deleted'})
        
        
class AllOrdersView(APIView):
    
    permission_classes = (IsAuthenticated,IsAdminUser)
    
    def get(self,request):
                
        try:
            order = Order.objects.filter(status="Pending")
            serializer = OrderSerializer(order,many=True)
            
        except Exception as e :
              return Response({"detail":f"somethings went wrong. {str(e)}"})
        
        return Response(serializer.data) 
        
    
    def post(self,request):
        
        ser_data = OrederIdSerialaizer(data=request.data)
        
        if ser_data.is_valid():
            
            serialized_data = ser_data.data['ides']
            status={'status':'Sent'}
            try:
                for i in serialized_data:
                    
                    order = Order.objects.filter(id=i)
                    
                    if order.get().status == "Sent":
                        return Response({'detail':"this itme have been sent befor."})
                    
                    order.update(**status)
                    order = order.get()
                    email = order.customer.email
                    send_notification_mail(email,f"your order with id {i} have sended.")
                    
            except Exception as e:
                return Response({"detail":f"Error {str(e)}"})
            
        return Response({'message':'seccess'})
    
    
