from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from .phone_valitor import phone_validator,PhoneNumberField
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

class BaseModel(models.Model):
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract=True
        
class UserManager(BaseUserManager):

    def create_user(self, phone, password, **other_fields):
        if phone is None:
            raise ValueError("Phone not given")
        user = self.model(phone=phone, **other_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, phone, password=None, **other_fields):
        other_fields.setdefault('is_staff', True)
        other_fields.setdefault('is_superuser', True)

        if other_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if other_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(phone, password, **other_fields)

class User(AbstractBaseUser,PermissionsMixin,BaseModel):
    phone = PhoneNumberField(validators=[phone_validator], unique=True, max_length=20)
    email = models.EmailField(_("email address"), unique=True)
    date_joined = models.DateTimeField(default=timezone.now)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    objects = UserManager()

    USERNAME_FIELD = 'phone'
    REQUIRED_FIELDS = []

    def __str__(self):
        return f"{self.phone}"


class Address(BaseModel):
    
    province = models.CharField(max_length=50,)
    city = models.CharField(max_length=50)
    street = models.CharField(max_length=50)
    number = models.IntegerField()
    other_details = models.TextField(blank=True,null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE,related_name='address')
    
    
    def __str__(self):
        return f"{self.province},{self.city},{self.street},{self.number},{self.other_details}"
    
    @property
    def user_address(self):
        user_address = Address.objects.get(user=self.user)
        return user_address
    
    
class Profile(BaseModel):
    
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    image = models.ImageField()
    user = models.ForeignKey(User,on_delete=models.CASCADE,related_name='profile')
    
    def __str__(self):
        return f"{self.first_name}"
    