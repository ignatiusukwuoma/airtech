from django.forms import Form, ModelChoiceField, DateField, IntegerField, CharField, EmailField, DateInput, Select
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Location
from .utils import tomorrow


class MyDateInput(DateInput):
    input_type = 'date'


class MyDateField(DateField):
    widget = MyDateInput


class SearchFlights(Form):
    from_location = ModelChoiceField(queryset=Location.objects.all(),
                                     empty_label='Select Airport',
                                     label='From',
                                     widget=Select(attrs={'placeholder': 'From'}))
    to_location = ModelChoiceField(queryset=Location.objects.all(),
                                   empty_label='Select Airport',
                                   label='To',
                                   widget=Select(attrs={'placeholder': 'To'}))
    departure_date = MyDateField(label='Departing',
                                 widget=MyDateInput(attrs={'min': tomorrow}))
    returning_date = MyDateField(label='Returning',
                                 required=False,
                                 widget=MyDateInput(attrs={'min': tomorrow}))
    adults = IntegerField(min_value=0, max_value=5)
    children = IntegerField(min_value=0, max_value=5, required=False)
    infants = IntegerField(min_value=0, max_value=5, required=False)


class FlightStatusByAirport(Form):
    from_location = ModelChoiceField(queryset=Location.objects.all(),
                                     empty_label='Select Airport',
                                     label='From')
    to_location = ModelChoiceField(queryset=Location.objects.all(),
                                   empty_label='Select Airport',
                                   label='To')
    departure_date = MyDateField(label='Flight Date')


class FlightStatusByNumber(Form):
    flight_number = CharField(max_length=20)


class SignUpForm(UserCreationForm):
    first_name = CharField(max_length=30, required=False)
    last_name = CharField(max_length=30, required=False)
    email = EmailField(max_length=254)

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2')

