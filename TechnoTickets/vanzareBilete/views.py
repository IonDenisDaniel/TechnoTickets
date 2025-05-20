from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.

def home(request):
    return render(request, 'vanzareBilete/home.html')

def events(request):
    return render(request, 'vanzareBilete/events.html')

def contactUs(request):
    return render(request, 'vanzareBilete/contactUs.html')
