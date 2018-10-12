import uuid

from django.db.models import Model, ForeignKey, CASCADE, SET_NULL, CharField, DateField, EmailField
from django.core.validators import RegexValidator


def generate_e_ticket():
    return uuid.uuid4().hex[:6].upper()


class TicketStatus(Model):
    name = CharField(max_length=30)


class Ticket(Model):
    """A model defining a Ticket"""

    ECONOMY = 'E'
    BUSINESS = 'B'
    CLASS = (
        (ECONOMY, 'Economy'),
        (BUSINESS, 'Business')
    )

    flight = ForeignKey('flights.Flight', on_delete=CASCADE)
    ticket_status = ForeignKey(TicketStatus, on_delete=CASCADE)
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


class Trip(Model):
    """A model defining a Trip"""
    phone_regex = RegexValidator(regex=r'^0\d{10}$', message="Enter a Nigerian mobile phone number")

    passenger_name = CharField(max_length=254)
    passenger_dob = DateField()
    passenger_email = EmailField(max_length=254)
    passenger_phone = CharField(validators=[phone_regex], max_length=11)
    departure_ticket_1 = ForeignKey(Ticket, on_delete=SET_NULL, null=True, related_name='a_ticket_1')
    departure_ticket_2 = ForeignKey(Ticket, on_delete=SET_NULL, null=True, related_name='a_ticket_2')
    arrival_ticket_1 = ForeignKey(Ticket, on_delete=SET_NULL, null=True, related_name='d_ticket_1')
    arrival_ticket_2 = ForeignKey(Ticket, on_delete=SET_NULL, null=True, related_name='d_ticket_2')
