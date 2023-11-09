from .serializers import UserSerializer,AddressSerializer,Profileserializer,UserInfoSerializer
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import AuthenticationFailed 
from .models import User,Address,Profile
from django.db.models import Q
from .phone_valitor import phone_validator,PhoneNumberField
from .token_jwt import create_access_token,create_refresh_token,decode_refresh_token
from .cache import setKey,set_code,get_code,deleteKey,getKey
from uuid import uuid4
from user.tasks import send_notification_mail,send_otp_mail
import random

class RigisterView(APIView):
    def post(self,request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            print(serializer.validated_data["phone"])
            if  User.objects.filter(Q(email__iexact=serializer.validated_data["email"]) | Q(phone__iexact=PhoneNumberField.get_prep_value(self,serializer.validated_data["phone"]))).first():
                    raise AuthenticationFailed(detail="The email or phone is already existe.")    
            User.objects.create_user(
                phone = serializer.validated_data["phone"],
                email = serializer.validated_data["email"],
                password = serializer.validated_data["password"]
            )
            send_notification_mail.delay(serializer.validated_data["email"],"you are seccessfully registered.")
            return Response(serializer.data)
        return Response(serializer.errors)
 

class LoginView(APIView):
    
    def post(self,request):
        email_or_phone:str =request.data['email_or_phone']
        password = request.data['password']
        
        if email_or_phone.isdigit() or email_or_phone.startswith("+"):
            email_or_phone = PhoneNumberField.get_prep_value(self,email_or_phone)   
                 
        user = User.objects.filter(Q(email__iexact=email_or_phone) | Q(phone__iexact=email_or_phone)).first()

        if user is None:
            raise AuthenticationFailed('User not found')
        
        if not user.check_password(password):
            raise AuthenticationFailed('Incorrect password')
        
        otp = str(random.randint(1000,9999))
        x=set_code(user.email,otp,90)
        # print(x)
        send_otp_mail.delay(user.email,f"Your code is {otp}")

        return Response({"detail":"code have been sended"})
        
        
        
        
class VerifyView(APIView):
    
    jti = uuid4().hex
    
    def post(self,request):
        email_or_phone:str =request.data['email_or_phone']
        get_otp:str = request.data["otp"]
        user = User.objects.filter(email__iexact=email_or_phone).first()
        # print(get_otp)
        # print(get_code(email_or_phone))
        if (otp := get_code(email_or_phone)):
            # print(F"{otp} from verify")
            if otp == get_otp:
                token={
                    'access_token':create_access_token(user.id,self.jti),
                    'refresh_token':create_refresh_token(user.id,self.jti) 
                }
                setKey(self.jti,user.id)
                send_notification_mail.delay(user.email,"you are logged in.")
                return Response(token)
            else:
                raise AuthenticationFailed("your code not match.")
        else:
            raise AuthenticationFailed("Somethings went wrong.")
        
        
class AuthenticateRefreshToken(APIView):
    jti = uuid4().hex
    
    def get(self,request):
        refresh_token = request.GET['refresh_token']
    
        if refresh_token is None:
            raise AuthenticationFailed('token not found')
        
        id = decode_refresh_token(refresh_token)
        
        return Response({
            'access_token':create_access_token(id,self.jti),
            'refresh_token':create_refresh_token(id,self.jti)   
        })
        
        
class LogoutView(APIView):
    
    permission_classes = (IsAuthenticated,)

    def get(self,request):
        
        try:
            payload = request.auth
            jti = payload["jti"]
            deleteKey(jti)
            
            return Response({"message": "Logged out successfully"}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"message": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        
        


class AddressView(APIView):
    
    permission_classes = (IsAuthenticated,)
    
    def post(self,request):
        user = request.user
        serializer = AddressSerializer(data=request.data)
        
        if serializer.is_valid():
            Address.objects.create(user=user,**serializer.data)
            return Response({'message':"address added"})

        return Response({'detail':'somethings went wrong.'})    
        
    def get(self,request):
        user = request.user
        try:
            address = Address.objects.get(user=user)
        except Exception as e :
            return Response({"detail":f"somethings went wrong.{str(e)}"})
        serializer = AddressSerializer(address)
        return Response(serializer.data) 
    
    
    def put(self,request):
        user = request.user
        serializer = AddressSerializer(data=request.data)
        if serializer.is_valid():
            ser_data = serializer.data
            ser_data = {key: value for key, value in ser_data.items() if value is not None}
            Address.objects.filter(user=user).update(**serializer.data)
            return Response({'message':"address updated"})
        
        return Response({'detail':'somethings went wrong.'}) 
    

class ProfileView(APIView):
    
    permission_classes = (IsAuthenticated,)
    
    def post(self,request):
        user = request.user
        serializer = Profileserializer(data=request.data)
        
        if serializer.is_valid():
            Profile.objects.create(user=user,**serializer.data)
            return Response({'message':"profile updated"})

        return Response({'detail':'somethings went wrong.'}) 
        
    
    
    def get(self,request):
        user = request.user
        try:
            address = Profile.objects.get(user=user)
        except Exception as e :
            return Response({"detail":f"somethings went wrong. {str(e)}"})
        serializer = Profileserializer(address)
        return Response(serializer.data) 
    
    def put(self,request):
        user = request.user
        serializer = Profileserializer(data=request.data)
        if serializer.is_valid():
            ser_data = serializer.data
            ser_data = {key: value for key, value in ser_data.items() if value is not None}
            Profile.objects.filter(user=user).update(**serializer.data)
            return Response({'message':"Profile updated"})
        
        return Response({'detail':'somethings went wrong.'})
        

class UserInfoView(APIView):
    
    permission_classes = (IsAuthenticated,)
    
    def get(self,request):
        user = request.user
        try:
            user = User.objects.get(id=user.id)
        except Exception as e :
            return Response({"detail":f"somethings went wrong. {str(e)}"})
        serializer =UserInfoSerializer(user)
        return Response(serializer.data) 
        
        
        
class AdminRegisterView(APIView):
    
    def post(self,request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            print(serializer.validated_data["phone"])
            if  User.objects.filter(Q(email__iexact=serializer.validated_data["email"]) | Q(phone__iexact=PhoneNumberField.get_prep_value(self,serializer.validated_data["phone"]))).first():
                    raise AuthenticationFailed(detail="The email or phone is already existe.")    
            User.objects.create_user(
                is_staff=True,
                phone = serializer.validated_data["phone"],
                email = serializer.validated_data["email"],
                password = serializer.validated_data["password"]
            )
            send_notification_mail.delay(serializer.validated_data["email"],"you are seccessfully registered.")
            return Response(serializer.data)
        return Response(serializer.errors)
        
