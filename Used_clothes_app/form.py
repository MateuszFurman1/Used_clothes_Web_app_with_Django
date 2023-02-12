from datetime import datetime
from django.core.validators import RegexValidator
from django.contrib.auth import get_user_model
from django import forms
from django.core.exceptions import ValidationError
from Used_clothes_app.models import User


class LoginForm(forms.Form):
    email = forms.EmailField(widget=forms.TextInput(
        attrs={'placeholder': 'Email'}))
    password = forms.CharField(
        max_length=128, widget=forms.PasswordInput(attrs={'placeholder': 'Hasło'}))


class RegistrationForm(forms.ModelForm):
    password = forms.CharField(
        max_length=128, widget=forms.PasswordInput(attrs={'placeholder': 'Hasło'}))
    re_password = forms.CharField(max_length=128, widget=forms.PasswordInput(
        attrs={'placeholder': 'Powtórz Hasło'}))

    class Meta:
        model = get_user_model()
        fields = ['email', 'first_name',
                  'last_name', 'password', 're_password']
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
    password = forms.CharField(
        widget=forms.PasswordInput, label="Confirm using your password")

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")

        # Get the current user
        user = User.objects.get(email=self.request.user.email)

        # Compare the password from the form to the user's password
        if not user.check_password(password):
            raise forms.ValidationError("Incorrect password")
        return cleaned_data


# class ChangePasswordForm(forms.Form):
    # old_password = forms.CharField(widget=forms.PasswordInput)
    # new_password = forms.CharField(widget=forms.PasswordInput)
    # confirm_password = forms.CharField(widget=forms.PasswordInput)

    # def __init__(self, user, *args, **kwargs):
    #     self.user = user
    #     super().__init__(*args, **kwargs)

    # def clean_old_password(self):
    #     old_password = self.cleaned_data.get('old_password')

    #     if not self.user.check_password(old_password):
    #         raise forms.ValidationError("Old password is incorrect.")

    #     return old_password

    # def clean_confirm_password(self):
    #     new_password = self.cleaned_data.get('new_password')
    #     confirm_password = self.cleaned_data.get('confirm_password')

    #     if new_password != confirm_password:
    #         raise forms.ValidationError("Confirm password does not match.")

    #     return confirm_password

    # def save(self, commit=True):
    #     self.user.set_password(self.cleaned_data["new_password"])
    #     if commit:
    #         self.user.save()
    #     return self.user


phone_regex = RegexValidator(
    regex=r'^\+?1?\d{9,15}$',
    message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed."
)


class DonationForm(forms.Form):
    quantity = forms.IntegerField()
    categories = forms.CharField(max_length=128)
    institution = forms.CharField(max_length=128)
    address = forms.CharField(max_length=128)
    phone_number = forms.IntegerField(validators=[phone_regex])
    city = forms.CharField(max_length=128)
    zip_code = forms.CharField(max_length=128)
    pick_up_date = forms.DateField()
    pick_up_time = forms.TimeField()
    pick_up_comment = forms.CharField(max_length=128)
    is_taken = forms.BooleanField(
        initial=False, required=False, label='Odebrane:', widget=forms.CheckboxInput())

    def clean_quantity(self):
        quantity = self.cleaned_data['quantity']
        if quantity <= 0:
            raise ValidationError('Quantity must be greater than zero!')
        return quantity

    def clean_pick_up_date(self):
        today = datetime.date.today()
        pick_up_date = self.cleaned_data['pick_up_date']
        if pick_up_date < today():
            raise ValidationError('Pick up date must be in the future!')
