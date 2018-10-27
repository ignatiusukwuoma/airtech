from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import PassportForm, PassengerForm, ContactForm
from .utils import get_passenger_list


def booking(request):
    if request.method == 'GET':
        form = PassengerForm()
        passengers = request.session.pop('passengers', None)
        list_of_passengers = get_passenger_list(passengers)

        request.session['passenger_list'] = list_of_passengers
        request.session['passengers'] = {}
        current_passenger = 'Adult 1'
        request.session['current_passenger'] = current_passenger

    if request.method == 'POST':
        current_passenger = request.session['current_passenger']
        form = ContactForm(request.POST) if current_passenger == 'Contact details' else PassengerForm(request.POST)

        if form.is_valid():
            list_of_passengers = request.session.pop('passenger_list')
            filled_passenger, filled_passenger_key = list_of_passengers.pop(0)

            request.session['passengers'][filled_passenger_key] = form.cleaned_data
            request.session.modified = True

            if list_of_passengers:
                current_passenger, passenger_key = list_of_passengers[0]

                request.session['passenger_list'] = list_of_passengers
                request.session['current_passenger'] = current_passenger

                form = ContactForm() if passenger_key == 'contact' else PassengerForm()
                return render(request, 'booking.html',
                              {'title': 'Booking',
                               'price': request.session['price'],
                               'form': form,
                               'passenger': current_passenger})
            else:
                try:
                    del request.session['current_passenger']
                except KeyError:
                    pass
                return redirect('summary')

    return render(request, 'booking.html',
                  {'title': 'Booking',
                   'form': form,
                   'price': request.session['price'],
                   'passenger': current_passenger})


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
    passengers = request.session['passengers']
    flights = request.session['flights']

    return render(request, 'summary.html',
                  {'title': 'summary'})

