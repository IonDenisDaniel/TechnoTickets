from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from .forms import UserFormCreation

# Create your views here.

def home(request):
    return render(request, 'vanzareBilete/home.html')

def events(request):
    return render(request, 'vanzareBilete/events.html')

def contactUs(request):
    return render(request, 'vanzareBilete/contactUs.html')

def Register(request):

    form = UserFormCreation()
    if request.method == 'POST':
        form = UserFormCreation(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')

    context = {
        'form': form
    }
    return render(request, 'vanzareBilete/register.html', context)
