import uuid
from django.core.validators import RegexValidator

phone_regex = RegexValidator(regex=r'^0\d{10}$', message="Please enter a Nigerian mobile phone number")


def generate_e_ticket():
    return uuid.uuid4().hex[:6].upper()


def generate_uuid():
    return uuid.uuid4().hex.upper()


def get_passenger_list(passengers):
    contact = ('Contact details', 'contact')
    if passengers:
        passenger_list = [(f"{k} {x}", f"{k}{x}") for k, v in passengers.items() if v for x in range(1, v + 1)]
        passenger_list.append(contact)
    else:
        passenger_list = []
    return passenger_list

