from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, SetPasswordForm
from .forms import UserFormCreation, CustomUserCreationForm, updateCustomUserFirstNameForm, updateCustomUserLastNameForm, updateCustomUserEmailForm, updateCustomUserProfilePictureForm
from django.contrib import messages

from django.contrib.auth import authenticate, login, logout

from django.contrib.auth.decorators import login_required
from .decorators import unauthenticated_user

from .models import Event,Ticket

from.functions import mostPopular

#pentru mail
from django.core.mail import send_mail

# Create your views here.


def home(request):
    lista_bilete = Ticket.objects.all()
    lista_bilete_populare = mostPopular(lista_bilete)
    lista = []
    for k,v in lista_bilete_populare.items():
        event = Event.objects.get(denumire = k)
        lista.append(event)

    lista_evenimente_recente = Event.objects.order_by('data')

    context = {
        'lista_evenimente_populare': lista[0:4],
        'lista_evenimente_recente': lista_evenimente_recente[0:4]
    }

    return render(request, 'vanzareBilete/home.html', context)

def events(request):
    lista_evenimente = Event.objects.all()

    context = {
        'lista_evenimente': lista_evenimente
    }
    return render(request, 'vanzareBilete/events.html', context)

def contactUs(request):
    if request.method == 'POST':
        nume = request.POST.get('nume')
        email = request.user.email
        subiect = request.POST.get('subiect')
        mesaj = request.POST.get('mesaj')
        mesaj = f"{request.user.nume} {request.user.prenume} \n {subiect} \n {mesaj}"

        send_mail(
            subject = subiect,
            message = mesaj,
            from_email = email,
            recipient_list = ['DENIS_NOLIMITS@yahoo.com']
        )

        return redirect('/')
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
    user = request.user
    lista_bilete = Ticket.objects.filter(owner = user)
    lista_evenimente = []
    for bilet in lista_bilete:
        lista_evenimente.append(bilet.event)

    context = {
        'lista_evenimente': lista_evenimente
    }
    return render(request, 'vanzareBilete/myAccount.html', context)


def updateUserFirstName(request):
    user = request.user
    form = updateCustomUserFirstNameForm(instance=user)
    if request.method == 'POST':
        form = updateCustomUserFirstNameForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            return redirect('my_account')

    context = {
        'form': form
    }
    return render(request, 'vanzareBilete/updateUserFirstNameForm.html', context)

def updateUserLastName(request):
    user = request.user
    form = updateCustomUserLastNameForm(instance=user)
    if request.method == 'POST':
        form = updateCustomUserLastNameForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            return redirect('my_account')

    context = {
        'form': form
    }
    return render(request, 'vanzareBilete/updateUserLastNameForm.html', context)

def updateUserEmail(request):
    user = request.user
    form = updateCustomUserEmailForm(instance=user)
    if request.method == 'POST':
        form = updateCustomUserEmailForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            return redirect('my_account')
        
    context = {
        'form': form
    }
    return render(request, 'vanzareBilete/updateUserEmailForm.html', context)

def updateUserPassword(request):
    user = request.user
    form = SetPasswordForm(user)
    if request.method == 'POST':
        form = SetPasswordForm(user, request.POST)
        if form.is_valid():
            form.save()
            return redirect('my_account')
        
    context = {
        'form': form
    }
    return render(request, 'vanzareBilete/updateUserPasswordForm.html', context)


def updateUserProfilePicture(request):
    user = request.user
    form = updateCustomUserProfilePictureForm(instance=user)
    if request.method == 'POST':
        form = updateCustomUserProfilePictureForm(request.POST, request.FILES, instance=user)
        if form.save():
            form.save()
            return redirect('my_account')
        
    context = {
        'form': form
    }
    return render(request, 'vanzareBilete/updateUserProfilePictureForm.html', context)