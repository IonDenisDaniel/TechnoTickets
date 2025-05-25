from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from .forms import UserFormCreation, CustomUserCreationForm
from django.contrib import messages

from django.contrib.auth import authenticate, login, logout

from django.contrib.auth.decorators import login_required
from .decorators import unauthenticated_user

from .models import Event

# Create your views here.


def home(request):
    return render(request, 'vanzareBilete/home.html')

def events(request):
    lista_evenimente = Event.objects.all()

    context = {
        'lista_evenimente': lista_evenimente
    }
    return render(request, 'vanzareBilete/events.html', context)

def contactUs(request):
    return render(request, 'vanzareBilete/contactUs.html')

@unauthenticated_user
def Register(request):
    form = CustomUserCreationForm()
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')

    context = {
        'form': form
    }
    return render(request, 'vanzareBilete/register.html', context)

@unauthenticated_user
def LogIn(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        user = authenticate(request, email = email, password = password)

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.info(request, 'Username or password is incorectly.')

    context = {}
    return render(request, 'vanzareBilete/login.html', context)


def LogOut(request):
    logout(request)
    return redirect('home')

@login_required(login_url='log_in')
def MyAccount(request):
    context = {}
    return render(request, 'vanzareBilete/myAccount.html', context)