from django.db.models import Model, ForeignKey, CASCADE, CharField, DateField, EmailField, OneToOneField,\
    ImageField, PositiveSmallIntegerField, BooleanField
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

from .utils import generate_e_ticket, generate_uuid, phone_regex


class Profile(Model):
    user = OneToOneField(User, on_delete=CASCADE)
    passport = ImageField(upload_to='images/')
    phone = CharField(validators=[phone_regex], max_length=11)

    @receiver(post_save, sender=User)
    def save_user_profile(sender, instance, created, **kwargs):
        if created:
            Profile.objects.create(user=instance)
        else:
            instance.profile.save()


class BookingStatus(Model):
    name = CharField(max_length=30)

    def __str__(self):
        return self.name


class Booking(Model):
    """A model defining a Booking"""

    e_booking = CharField(max_length=32, unique=True, blank=True, default=generate_uuid)
    user = ForeignKey(User, on_delete=CASCADE, blank=True, null=True)
    booking_status = ForeignKey(BookingStatus, on_delete=CASCADE, default=1)
    contact_first_name = CharField(max_length=100)
    contact_last_name = CharField(max_length=100)
    contact_email = EmailField(max_length=254)
    contact_phone = CharField(validators=[phone_regex], max_length=11)

    def __str__(self):
        return f"Booking {self.id} - {self.booking_status}"


class Trip(Model):
    """A model defining a Trip"""

    passenger_first_name = CharField(max_length=100)
    passenger_last_name = CharField(max_length=100)
    passenger_age = PositiveSmallIntegerField()
    booking = ForeignKey(Booking, on_delete=CASCADE)

    def __str__(self):
        return f"Trip {self.id}"


class TicketClass(Model):
    """A model defining a Ticket class"""
    title = CharField(max_length=30)

    def __str__(self):
        return self.title


class Ticket(Model):
    """A model defining a Ticket"""

    ECONOMY = 'economy'
    BUSINESS = 'business'
    CLASS = (
        (ECONOMY, 'Economy'),
        (BUSINESS, 'Business')
    )

    flight = ForeignKey('flights.Flight', on_delete=CASCADE)
    trip = ForeignKey(Trip, on_delete=CASCADE)
    booking = ForeignKey(Booking, on_delete=CASCADE)
    ticket_class = CharField(max_length=10, choices=CLASS)
    e_ticket = CharField(max_length=10, unique=True, blank=True)
    issue_date = DateField(auto_now_add=True)
    reminder_sent = BooleanField(default=False)

    def __str__(self):
        return f"{self.ticket_class} ticket for {self.flight}"

    def save(self, *args, **kwargs):
        if not self.e_ticket:
            while True:
                ticket = generate_e_ticket()
                if not Ticket.objects.filter(e_ticket=ticket).exists():
                    break
            self.e_ticket = ticket
        super().save(*args, **kwargs)
