from django import forms
from django.contrib.auth.forms import UserCreationForm
from accounts.models import User
from django.core.exceptions import ValidationError
import datetime
from django.forms.extras.widgets import SelectDateWidget
from django.forms import ModelForm, Form

class UserRegistrationForm(UserCreationForm):
    password1 = forms.CharField(
        label='Password',
        widget=forms.PasswordInput
    )

    password2 = forms.CharField(
        label='Password Confirmation',
        widget=forms.PasswordInput
    )

    class Meta:
        model = User
        fields = ['email', 'password1', 'password2']
        exclude = ['username']

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')

        if password1 and password2 and password1 != password2:
            message = "Passwords do not match"
            raise ValidationError(message)

        return password2

    def save(self, commit=True):
        instance = super(UserRegistrationForm, self).save(commit=False)

        # automatically set to email address to create a unique identifier
        instance.username = instance.email

        if commit:
            instance.save()

        return instance


class UserLoginForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)

    class UserRegistrationForm(UserCreationForm):
        MONTH_CHOICES = [(i, i,) for i in xrange(1, 12)]
        YEAR_CHOICES = [(i, i,) for i in xrange(2015, 2036)]

        credit_card_number = forms.CharField(label='Credit card number')
        cvv = forms.CharField(label='Security code (CVV)')
        expiry_month = forms.ChoiceField(label="Month", choices=MONTH_CHOICES)
        expiry_year = forms.ChoiceField(label="Year", choices=YEAR_CHOICES)
        stripe_id = forms.CharField(widget=forms.HiddenInput)
        password1 = forms.CharField(
            label='Password',
            widget=forms.PasswordInput
        )

        password2 = forms.CharField(
            label='Password Confirmation',
            widget=forms.PasswordInput
        )

        class Meta:
            model = User
            fields = ['email', 'password1', 'password2', 'stripe_id']
            exclude = ['username']


class ContactForm(forms.Form):

    First_Name = forms.CharField(required=True)
    Last_Name = forms.CharField(required=True)
    Email = forms.EmailField(required=True)
    Subject = forms.CharField(required=True)
    Message = forms.CharField(widget=forms.Textarea)


class ReservationForm(forms.Form):
    Name = forms.CharField(required=True)
    Surname = forms.CharField(required=True)
    Email = forms.EmailField(required=True)
    Date = forms.DateField(widget=SelectDateWidget)
    Telephone = forms.CharField(required=True)
    Time = forms.TimeField(required=True)
    Guests = forms.IntegerField(required=True)

