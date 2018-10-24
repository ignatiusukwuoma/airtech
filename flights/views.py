from django.contrib.auth import login, authenticate
from django.shortcuts import render, redirect
from .forms import SearchFlights, FlightStatusByAirport, FlightStatusByNumber, SignUpForm
from .models import Flight
from .utils import flight_date_range, generate_flight_dates


def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(request, username=username, password=raw_password)
            if user is not None:
                login(request, user)
            return redirect('index')
    else:
        form = SignUpForm()
    return render(request, 'signup.html', {'form': form})


def index(request):
    search_flights = SearchFlights()
    flight_status_by_airport = FlightStatusByAirport()
    flight_status_by_number = FlightStatusByNumber()
    return render(request, 'index.html',
                  {'title': 'Home',
                   'search_flights': search_flights,
                   'flight_status_by_airport': flight_status_by_airport,
                   'flight_status_by_number': flight_status_by_number})


def flights(request):
    if request.method == 'POST':
        form = SearchFlights(request.POST)
        if form.is_valid():
            search = form.cleaned_data
            departure_date_range = flight_date_range(search['departure_date'])
            departure_results = list(Flight.objects.filter(
                departure=search['from_location'],
                destination=search['to_location'],
                scheduled__date__range=departure_date_range))
            departure_flights = generate_flight_dates(departure_date_range, departure_results)
            return_flights = None
            if search['returning_date']:
                return_date_range = flight_date_range(search['returning_date'])
                return_results = list(Flight.objects.filter(
                    departure=search['to_location'],
                    destination=search['from_location'],
                    scheduled__date__range=return_date_range))
                return_flights = generate_flight_dates(return_date_range, return_results)

            return render(request, 'flights.html',
                          {'title': 'Flights Now',
                           'departure_flights': departure_flights,
                           'return_flights': return_flights,
                           'search': search,
                           'form': form})
    return render(request, 'flights.html', {'title': 'Flights'})


def flight_status(request):
    if request.method == 'POST':
        status_by_airport = FlightStatusByAirport(request.POST) if 'from_location' in request.POST else None
        status_by_number = FlightStatusByNumber(request.POST) if 'flight_number' in request.POST else None
        flight = None
        if status_by_number and status_by_number.is_valid():
            query = status_by_number.cleaned_data
            flight = Flight.objects.filter(flight_number=query['flight_number'])
        elif status_by_airport and status_by_airport.is_valid():
            query = status_by_airport.cleaned_data
            flight = Flight.objects.filter(
                departure=query['from_location'],
                destination=query['to_location'],
                scheduled__date=query['departure_date'])

        if status_by_number:
            status_by_airport = FlightStatusByAirport()
        else:
            status_by_number = FlightStatusByNumber()

        return render(request, 'flight_status.html',
                      {'title': 'Check flight status',
                       'flights': flight,
                       'flight_status_by_number': status_by_number,
                       'flight_status_by_airport': status_by_airport})
    return render(request, 'flight_status.html', {'title': 'Check flight status'})

# import pdb;
 # pdb.set_trace()