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
        widgets = {
                'prenume':  forms.TextInput(attrs={'class': 'input', 'placeholder': 'Fisrt name...'}),
                'nume': forms.TextInput(attrs={'class': 'input','placeholder': 'Last name...'}),
                'email': forms.EmailInput(attrs={'class': 'input','placeholder': 'Email...'}),
            }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password1'].widget.attrs.update({'class': 'input', 'placeholder': 'Password...'})
        self.fields['password2'].widget.attrs.update({'class': 'input', 'placeholder': 'Repeat password...'})

class updateCustomUserFirstNameForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['prenume']

class updateCustomUserLastNameForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['nume']

class updateCustomUserEmailForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['email']




