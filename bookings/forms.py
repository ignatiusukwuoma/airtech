from django.forms import Form, ImageField


class PassportForm(Form):
    passport = ImageField(label='Select a file')
