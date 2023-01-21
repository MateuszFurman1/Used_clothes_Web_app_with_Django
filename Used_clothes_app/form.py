from django.contrib.auth import get_user_model
from django import forms
from xdg.Exceptions import ValidationError
from Used_clothes_app.models import User, Donation


class LoginForm(forms.Form):
    email = forms.EmailField(widget=forms.TextInput(attrs={'placeholder': 'Email'}))
    password = forms.CharField(max_length=128, widget=forms.TextInput(attrs={'placeholder': 'Hasło'}))


class RegistrationForm(forms.ModelForm):
    password = forms.CharField(max_length=128, widget=forms.TextInput(attrs={'placeholder': 'Hasło'}))
    re_password = forms.CharField(max_length=128, widget=forms.TextInput(attrs={'placeholder': 'Powtórz Hasło'}))

    class Meta:
        model = get_user_model()
        fields = ['email', 'first_name', 'last_name', 'password', 're_password']
        widgets = {
            'email': forms.EmailInput(attrs={'placeholder': 'Email'}),
            'first_name': forms.TextInput(attrs={'placeholder': 'Imię'}),
            'last_name': forms.TextInput(attrs={'placeholder': 'Nazwisko'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        if cleaned_data['password'] != cleaned_data['re_password']:
            raise ValidationError('Passwords are not the same!')


class ProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']


class DonationForm(forms.Form):
    quantity = forms.IntegerField()
    categories = forms.CharField(max_length=128)
    institution = forms.CharField(max_length=128)
    address = forms.CharField(max_length=128)
    phone_number = forms.IntegerField()
    city = forms.CharField(max_length=128)
    zip_code = forms.CharField(max_length=128)
    pick_up_date = forms.DateField()
    pick_up_time = forms.TimeField()
    pick_up_comment = forms.CharField(max_length=128)