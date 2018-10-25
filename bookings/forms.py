from django.forms import ModelForm
from .models import Profile


class PassportForm(ModelForm):
    class Meta:
        model = Profile
        fields = ['passport']
