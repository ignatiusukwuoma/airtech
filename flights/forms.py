from django.forms import Form, ModelChoiceField, DateField, IntegerField, CharField, DateInput, Select
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
    adults = IntegerField(max_value=5)
    children = IntegerField(max_value=5, required=False)
    infants = IntegerField(max_value=5, required=False)


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

