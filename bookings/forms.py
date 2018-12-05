from django.forms import ModelForm, Form, CharField, EmailField, IntegerField, ChoiceField, RadioSelect, DateField
from .models import Profile
from .utils import phone_regex, AIRTECH


class PassportForm(ModelForm):
    class Meta:
        model = Profile
        fields = ['passport']


class PassengerForm(Form):
    first_name = CharField(max_length=100)
    last_name = CharField(max_length=100)
    age = IntegerField(min_value=0, max_value=1000)


class ContactForm(Form):
    first_name = CharField(max_length=100)
    last_name = CharField(max_length=100)
    email = EmailField(max_length=254)
    phone = CharField(validators=[phone_regex], max_length=11)


class PayScheduleForm(Form):
    CHOICES = (('now', 'Pay Now',), ('later', 'Pay Later',))

    pay_choice = ChoiceField(widget=RadioSelect, choices=CHOICES)

    pay_choice.widget.attrs.update({'class': 'pay-choice'})


class PaymentForm(Form):
    card_number = CharField(max_length=30)
