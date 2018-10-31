import json
from multiprocessing.dummy import Pool as ThreadPool

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.http import HttpResponse

from flights.models import Flight
from .models import Booking, Trip, Ticket
from .utils import get_passenger_list, mail_tickets, CONTACT_ID, CONTACT_DETAILS
from .forms import PassportForm, PassengerForm, ContactForm, PaymentForm


def booking(request):
    if request.method == 'GET':
        form = PassengerForm()
        passengers = request.session['passengers']
        list_of_passengers = get_passenger_list(passengers)

        current_passenger = 'Adult 1'
        request.session['current_passenger'] = current_passenger
        request.session['passenger_list'] = list_of_passengers
        request.session['passenger_details'] = {}

    if request.method == 'POST':
        current_passenger = request.session['current_passenger']
        form = ContactForm(request.POST) if current_passenger == CONTACT_DETAILS else PassengerForm(request.POST)

        if form.is_valid():
            list_of_passengers = request.session.pop('passenger_list')
            filled_passenger, filled_passenger_key = list_of_passengers.pop(0)
            request.session['passenger_details'][filled_passenger_key] = form.cleaned_data
            request.session.modified = True

            if list_of_passengers:
                current_passenger, passenger_key = list_of_passengers[0]
                request.session['passenger_list'] = list_of_passengers
                request.session['current_passenger'] = current_passenger

                form = ContactForm() if passenger_key == CONTACT_ID else PassengerForm()
                return render(request,
                              'booking.html',
                              {'title': 'Booking',
                               'price': request.session['price'],
                               'passenger': current_passenger,
                               'form': form})
            else:
                try:
                    del request.session['current_passenger']
                except KeyError:
                    pass
                return redirect('summary')

    return render(request,
                  'booking.html',
                  {'title': 'Booking',
                   'price': request.session['price'],
                   'passenger': current_passenger,
                   'form': form})


@login_required
def profile(request):
    if request.method == 'POST':
        form = PassportForm(request.POST, request.FILES)
        if form.is_valid():
            passport = request.FILES['passport']
            user = request.user
            user.profile.passport = passport
            user.save()
    else:
        form = PassportForm()
    return render(request, 'profile.html', {'title': request.user.get_username(), 'form': form})


@login_required()
def delete_passport(request):
    if request.method == 'POST':
        request.user.profile.passport.delete()
    return redirect('profile')


def summary(request):
    if request.method == 'POST':
        data = request.body.decode(encoding='UTF-8')
        data_obj = json.loads(data)
        request.session['pay_schedule'] = data_obj['pay_schedule']
        response = json.dumps({'data': 'success'})
        return HttpResponse(content=response, content_type='application/json', status=200)

    passenger_details = request.session['passenger_details']
    passengers = request.session['passengers']
    flights = request.session['flights']
    outbound_flight_id = int(flights['outbound']['flightId'])
    outbound_flight = Flight.objects.get(id=outbound_flight_id)
    outbound_class = flights['outbound']['flightClass']
    inbound_flight = None
    inbound_class = None
    if flights['inbound']:
        inbound_flight_id = int(flights['inbound']['flightId'])
        inbound_flight = Flight.objects.get(id=inbound_flight_id)
        inbound_class = flights['inbound']['flightClass']

    return render(request,
                  'summary.html',
                  {'title': 'summary',
                   'passengers': passengers,
                   'passenger_details': passenger_details,
                   'total_price': request.session['price'],
                   'outbound_flight': outbound_flight,
                   'outbound_class': outbound_class,
                   'inbound_flight': inbound_flight,
                   'inbound_class': inbound_class})


def payment(request):
    if request.method == 'POST':
        form = PaymentForm(request.POST)
        if form.is_valid():
            passenger_details = request.session['passenger_details']
            user = None
            if request.user.is_authenticated:
                user = request.user
            booking_status = 1
            if request.session['pay_schedule'] == 'pay-now':
                booking_status = 2

            book_flight = Booking(
                        contact_first_name=passenger_details['contact']['first_name'],
                        contact_last_name=passenger_details['contact']['last_name'],
                        contact_email=passenger_details['contact']['email'],
                        contact_phone=passenger_details['contact']['phone'],
                        user=user,
                        booking_status_id=booking_status
            )
            book_flight.save()

            booking_list = []
            for passenger, details in passenger_details.items():
                if passenger != 'contact':
                    trip = Trip(
                        passenger_first_name=details['first_name'],
                        passenger_last_name=details['last_name'],
                        passenger_age=details['age'],
                        booking=book_flight
                    )
                    trip.save()

                    flights = request.session['flights']
                    departure_ticket = Ticket(
                        flight_id=flights['outbound']['flightId'],
                        trip=trip,
                        booking=book_flight,
                        ticket_class=flights['outbound']['flightClass']
                    )
                    departure_ticket.save()

                    arrival_ticket = None
                    if flights['inbound']:
                        arrival_ticket = Ticket(
                            flight_id=flights['inbound']['flightId'],
                            trip=trip,
                            booking=book_flight,
                            ticket_class=flights['inbound']['flightClass']
                        )
                        arrival_ticket.save()

                    this_booking = {
                        'booking': book_flight,
                        'trip': trip,
                        'departure_ticket': departure_ticket,
                        'arrival_ticket': arrival_ticket
                    }
                    booking_list.append(this_booking)

            pool = ThreadPool(4)
            results = pool.map(mail_tickets, booking_list)
            pool.close()
            pool.join()
            return redirect('success')

    else:
        form = PaymentForm()
    return render(request,
                  'payment.html',
                  {'title': 'Payment',
                   'form': form,
                   'price': request.session['price'],
                   'pay_schedule': request.session['pay_schedule']})


def success(request):
    return render(request, 'success.html', {'title': 'success'})
