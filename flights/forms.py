from django.forms import Form, ModelChoiceField, DateField, IntegerField, DateInput
from .models import Location


class MyDateInput(DateInput):
    input_type = 'date'


class MyDateField(DateField):
    widget = MyDateInput


class SearchFlights(Form):
    from_location = ModelChoiceField(queryset=Location.objects.all(),
                                     empty_label='Select Airport',
                                     label='From')
    to_location = ModelChoiceField(queryset=Location.objects.all(),
                                   empty_label='Select Airport',
                                   label='To')
    departure_date = MyDateField(label='Departing')
    returning_date = MyDateField(label='Returning', required=False)
    adults = IntegerField(max_value=5, required=False)
    children = IntegerField(max_value=5, required=False)
    infants = IntegerField(max_value=5, required=False)
