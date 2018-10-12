from django.shortcuts import render


def index(request):
    return render(request, 'index.html', {'title': 'Home'})


def flights(request):
    return render(request, 'flights.html', {'title': 'Flights'})
