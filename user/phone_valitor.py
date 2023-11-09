from django.db import models
from django.core.exceptions import ValidationError
import re
from rest_framework.exceptions import AuthenticationFailed 

PHONE_REGEX_PATTERN = r"(((\+|00)(98))|0)?(?P<operator>9\d{2})-?(?P<middle3>\d{3})-?(?P<last4>\d{4})"

def phone_validator(phone:str):
    if not (matched := re.fullmatch(PHONE_REGEX_PATTERN, phone.strip())):
        raise AuthenticationFailed("Invalid phone number")
    return matched


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
