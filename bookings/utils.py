import uuid
from django.core.validators import RegexValidator

phone_regex = RegexValidator(regex=r'^0\d{10}$', message="Please enter a Nigerian mobile phone number")


def generate_e_ticket():
    return uuid.uuid4().hex[:6].upper()


def generate_uuid():
    return uuid.uuid4().hex.upper()
