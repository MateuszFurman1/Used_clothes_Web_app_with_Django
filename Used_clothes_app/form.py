from django.contrib.auth import get_user_model
from django import forms
from xdg.Exceptions import ValidationError
from Used_clothes_app.models import User


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