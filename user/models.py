from django.db import models
import re
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.core.exceptions import ValidationError
from .phone_valitor import phone_validator
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


class PhoneNumberField(models.CharField):
    def get_prep_value(self, value):
        if value is None:
            return value

        try:
            regex = phone_validator(value)
        except ValidationError:
            raise

        phone_parts = regex.groupdict()
        phone = phone_parts["operator"]+phone_parts["middle3"]+phone_parts["last4"]
        return phone



class User(AbstractBaseUser, PermissionsMixin,BaseModel):
    phone = PhoneNumberField(validators=[phone_validator], unique=True, max_length=20)
    username = models.CharField(max_length=60)
    email = models.EmailField(_("email address"), unique=True)
    date_joined = models.DateTimeField(default=timezone.now)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    objects = UserManager()

    USERNAME_FIELD = 'phone'
    REQUIRED_FIELDS = []

    def __str__(self):
        return f"{self.phone}"


class Address(BaseModel):
    province = models.CharField(max_length=50)
    city = models.CharField(max_length=50)
    street = models.CharField(max_length=50)
    number = models.IntegerField()
    other_details = models.TextField()
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    
    
    def __str__(self):
        return f"{self.province}"