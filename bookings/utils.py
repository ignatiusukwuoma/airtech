import uuid
from django.core.validators import RegexValidator
from django.core.mail import send_mail

CONTACT_ID = 'contact'
CONTACT_DETAILS = 'Contact details'
phone_regex = RegexValidator(regex=r'^0\d{10}$', message="Please enter a Nigerian mobile phone number")


def generate_e_ticket():
    return uuid.uuid4().hex[:6].upper()


def generate_uuid():
    return uuid.uuid4().hex.upper()


def get_passenger_list(passengers):
    contact = (CONTACT_DETAILS, CONTACT_ID)
    if passengers:
        passenger_list = [(f"{k} {x}", f"{k}{x}") for k, v in passengers.items() if v for x in range(1, v + 1)]
        passenger_list.append(contact)
    else:
        passenger_list = []
    return passenger_list


def mail_tickets(flight_booking):
    subject, message, from_email, recipient_list = \
        construct_email(flight_booking['booking'], flight_booking['trip'], flight_booking['departure_ticket'])
    send_mail(subject, message, from_email, recipient_list)
    if flight_booking['arrival_ticket']:
        subject2, message2, from_email2, recipient_list2 = \
            construct_email(flight_booking['booking'], flight_booking['trip'], flight_booking['arrival_ticket'])
        send_mail(subject2, message2, from_email2, recipient_list2)
    return 'success'


def construct_email(booking, trip, ticket):
    subject = f"Ticket for {trip.passenger_first_name}'s flight to " \
              f"{ticket.flight.destination.city} " \
              f"from FlyAirtech"
    message = f"Congratulations, your flight has been booked\n " \
              f"E-Ticket: {ticket.e_ticket} \n " \
              f"Ticket Class: {ticket.ticket_class} \n " \
              f"Flight Details: Flight {ticket.flight.flight_number} from {ticket.flight.departure.city} to " \
              f"{ticket.flight.destination.city} \n " \
              f"Booking ID: {booking.e_booking}"
    from_email = 'igdefinition@gmail.com'
    recipient_list = [f"{booking.contact_email}"]
    return subject, message, from_email, recipient_list


