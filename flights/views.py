from django.shortcuts import render
from .forms import SearchFlights


def index(request):
    form = SearchFlights()
    return render(request, 'index.html', {'title': 'Home', 'form': form})


def flights(request):
    return render(request, 'flights.html', {'title': 'Flights'})
