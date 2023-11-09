from rest_framework import serializers
from .models import User,Address,Profile
from rest_framework.exceptions import AuthenticationFailed 
from .phone_valitor import phone_validator


class UserSerializer(serializers.Serializer):
    
    email = serializers.EmailField(required=True)
    phone = serializers.CharField(required=True,validators=[phone_validator])
    password = serializers.CharField(required=True,write_only=True)
    password2 = serializers.CharField(required=True,write_only=True)
    

    
    def validate(self, data):
        if data["password"] != data["password2"]:
            raise AuthenticationFailed("passwords must be match")
        return data
    

class AddressSerializer(serializers.Serializer):
    
    province = serializers.CharField(required=False,max_length=30)
    city = serializers.CharField(required=False,max_length=30)
    street = serializers.CharField(required=False,max_length=30)
    number = serializers.IntegerField(required=False)
    other_details = serializers.CharField(required=False)
                
    def validate(self, data):
        if data["number"]:
            if not isinstance(data['number'],int):
                raise Exception({'detail':"number must be integer."})
        return data
    
class Profileserializer(serializers.Serializer):
    
    first_name = serializers.CharField(max_length=50,required=False)
    last_name = serializers.CharField(max_length=50,required=False)
    image = serializers.ImageField(required=False)
    
    
class UserInfoSerializer(serializers.ModelSerializer):
    
    # profile = serializers.RelatedField(many=True,read_only=True)
    # address = serializers.RelatedField(many=True,read_only=True)
    profile = Profileserializer(many=True,read_only=True)
    address = AddressSerializer(many=True,read_only=True)

    class Meta:
        model = User
        fields = ['phone','email','date_joined','profile','address']
        
