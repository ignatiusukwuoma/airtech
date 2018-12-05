from datetime import timedelta
from django.utils import timezone
from django.core.management.base import BaseCommand
from django.core.mail import send_mail
from bookings.models import Ticket, Booking, Trip


class Command(BaseCommand):
    help = 'Send email reminder to customers a day before their flight'

    def add_arguments(self, parser):
        parser.add_argument('-d', '--days_before_flight', type=int,
                            help='Indicates days before flight for reminder to be sent')

    @staticmethod
    def get_tickets(days=1):
        now = timezone.now()
        tomorrow = now + timedelta(days=days)
        tickets = Ticket.objects.filter(
            flight__last_update__lte=tomorrow,
            flight__last_update__gte=now,
            reminder_sent=False
        )[:10]
        return tickets

    @staticmethod
    def construct_reminder_email(booking, trip, ticket):
        subject = f"Reminder for {trip.passenger_first_name}'s flight to " \
            f"{ticket.flight.destination.city} " \
            f"from FlyAirtech"
        message = f"We wish to inform you that your flight is within the next 24 hours\n " \
            f"E-Ticket: {ticket.e_ticket} \n " \
            f"Ticket Class: {ticket.ticket_class} \n " \
            f"Flight Details: Flight {ticket.flight.flight_number} from {ticket.flight.departure.city} to " \
            f"{ticket.flight.destination.city} \n " \
            f"Booking ID: {booking.e_booking}"
        from_email = 'reminders@flyairtech.com'
        recipient_list = [f"{booking.contact_email}"]
        return subject, message, from_email, recipient_list

    @staticmethod
    def send_reminder_email(self, tickets):
        if bool(tickets):
            for ticket in tickets:
                booking = Booking.objects.get(ticket=ticket)
                trip = Trip.objects.get(ticket=ticket)
                subject, message, from_email, recipient_list = self.construct_reminder_email(booking, trip, ticket)
                send_mail(subject, message, from_email, recipient_list)
                ticket.reminder_sent = True
                ticket.save()

    def handle(self, *args, **options):
        days_before_flight = options['days_before_flight']
        tickets = self.get_tickets(days_before_flight) if days_before_flight else self.get_tickets()
        self.send_reminder_email(tickets)
