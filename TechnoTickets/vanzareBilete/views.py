from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from .forms import UserFormCreation, CustomUserCreationForm
from django.contrib import messages

from django.contrib.auth import authenticate, login, logout

# Create your views here.

def home(request):
    return render(request, 'vanzareBilete/home.html')

def events(request):
    return render(request, 'vanzareBilete/events.html')

def contactUs(request):
    return render(request, 'vanzareBilete/contactUs.html')


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


def MyAccount(request):
    context = {}
    return render(request, 'vanzareBilete/myAccount.html', context)