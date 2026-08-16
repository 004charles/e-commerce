from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm

from .models import User


class MarketplaceAuthenticationForm(AuthenticationForm):
    username = forms.CharField(label="Utilizador ou email")


class MarketplaceUserCreationForm(UserCreationForm):
    email = forms.EmailField(label="Email")
    phone = forms.CharField(label="Telefone", max_length=30, required=False)

    class Meta:
        model = User
        fields = ("username", "email", "phone", "password1", "password2")


class ProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ("first_name", "last_name", "email", "phone")
        widgets = {
            "first_name": forms.TextInput(attrs={"class": "form-control account-form-control"}),
            "last_name": forms.TextInput(attrs={"class": "form-control account-form-control"}),
            "email": forms.EmailInput(attrs={"class": "form-control account-form-control"}),
            "phone": forms.TextInput(attrs={"class": "form-control account-form-control"}),
        }
