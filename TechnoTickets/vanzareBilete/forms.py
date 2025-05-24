from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from .models import CustomUser


class UserFormCreation(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

class CustomUserCreationForm(UserCreationForm):
    # nume = forms.CharField()
    # prenume = forms.CharField()
    # email = forms.EmailField()
    # password1 = forms.PasswordInput()
    # password2 = forms.PasswordInput()

    class Meta:
        model = CustomUser
        fields = ['nume', 'prenume', 'email', 'password1', 'password2']