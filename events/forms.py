from django import forms
from django.contrib.auth.models import User
from .models import Event, Booking, UserProfile

class UserSignup(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email' ,'password']

        widgets={
        'password': forms.PasswordInput(),
        }


class UserLogin(forms.Form):
    username = forms.CharField(required=True)
    password = forms.CharField(required=True, widget=forms.PasswordInput())


class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        exclude = ['organizer']

class UserProfileForm(forms.ModelForm):
    class Meta:
        Model = User
        fields = ['username', 'first_name', "last_name", 'email']


class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ['tickets']
