from django.forms import ModelForm
from .models import User
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import AuthenticationForm


class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]
    

class LoginForm(AuthenticationForm):
    class Meta:
        model = User
        fields = ["email", "password"]

        