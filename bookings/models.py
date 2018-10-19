from django.db.models import Model, ForeignKey, CASCADE, SET_NULL, CharField, DateField, EmailField
from django.core.validators import RegexValidator
from django.contrib.auth.models import User

from .utils import generate_e_ticket, generate_uuid


class BookingStatus(Model):
    name = CharField(max_length=30)


class Trip(Model):
    """A model defining a Trip"""

    passenger_name = CharField(max_length=254)
    passenger_dob = DateField()


class Booking(Model):
    """A model defining a Booking"""
    phone_regex = RegexValidator(regex=r'^0\d{10}$', message="Please enter a Nigerian mobile phone number")

    e_booking = CharField(max_length=32, unique=True, blank=True, default=generate_uuid)
    user = ForeignKey(User, on_delete=CASCADE, blank=True, null=True)
    booking_status = ForeignKey(BookingStatus, on_delete=CASCADE)
    contact_name = CharField(max_length=254)
    contact_email = EmailField(max_length=254)
    contact_phone = CharField(validators=[phone_regex], max_length=11)


class Ticket(Model):
    """A model defining a Ticket"""

    ECONOMY = 'E'
    BUSINESS = 'B'
    CLASS = (
        (ECONOMY, 'Economy'),
        (BUSINESS, 'Business')
    )

    flight = ForeignKey('flights.Flight', on_delete=CASCADE)
    trip = ForeignKey(Trip, on_delete=CASCADE)
    booking = ForeignKey(Booking, on_delete=CASCADE)

    ticket_class = CharField(max_length=1, choices=CLASS, default=ECONOMY)
    e_ticket = CharField(max_length=10, unique=True, blank=True)
    issue_date = DateField(auto_now_add=True)

    def save(self, *args, **kwargs):
        while True:
            ticket = generate_e_ticket()
            if not Ticket.objects.filter(e_ticket=ticket).exists():
                break
        self.e_ticket = ticket
        super().save(*args, **kwargs)


