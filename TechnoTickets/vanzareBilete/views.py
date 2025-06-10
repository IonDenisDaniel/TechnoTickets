from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, SetPasswordForm
import stripe.error
from .forms import UserFormCreation, CustomUserCreationForm, updateCustomUserFirstNameForm, updateCustomUserLastNameForm, updateCustomUserEmailForm, updateCustomUserProfilePictureForm
from django.contrib import messages

from django.contrib.auth import authenticate, login, logout

from django.contrib.auth.decorators import login_required
from .decorators import unauthenticated_user

from .models import Event,Ticket,CustomUser

from.functions import mostPopular

#pentru mail
from django.core.mail import send_mail


from django.conf import settings

import stripe
stripe.api_key = settings.STRIPE_SECRET_KEY


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
        if form.is_valid():
            form.save()
            return redirect('my_account')
        
    context = {
        'form': form
    }
    return render(request, 'vanzareBilete/updateUserProfilePictureForm.html', context)


def EventPage(request, primary_key):
    event = Event.objects.get(id = primary_key)
    user = request.user


    #EarlyBird ticket
    EarlyBird_product_id = 'prod_SSgQz884h3IWoO'
    EarlyBird_product = stripe.Product.retrieve(EarlyBird_product_id)
    EarlyBird_prices = stripe.Price.list(product=EarlyBird_product_id)
    EarlyBird_price = EarlyBird_prices.data[0]
    EarlyBird_price_final = EarlyBird_price.unit_amount / 100.0

    #General Entry ticket
    GeneralEntry_product_id = 'prod_SSgR4tYlHkRaRk'
    GeneralEntry_product = stripe.Product.retrieve(GeneralEntry_product_id)
    GeneralEntry_prices = stripe.Price.list(product=GeneralEntry_product_id)
    GeneralEntry_price = GeneralEntry_prices.data[0]
    GeneralEntry_price_final = GeneralEntry_price.unit_amount / 100.0

    #VIP ticket
    VIP_product_id = 'prod_SSgRGeyFf7CAsv'
    VIP_product = stripe.Product.retrieve(VIP_product_id)
    VIP_prices = stripe.Price.list(product=VIP_product_id)
    VIP_price = VIP_prices.data[0]
    VIP_price_final = VIP_price.unit_amount / 100.0


    if request.method == 'POST':
        if not request.user.is_authenticated:
            return redirect('log_in')
        
        EarlyBird_price_id = request.POST.get('EarlyBird_price_id')
        EarlyBird_quantity = request.POST.get('EarlyBird_quantity')
        GeneralEntry_price_id = request.POST.get('GeneralEntry_price_id')
        GeneralEntry_quantity = request.POST.get('GeneralEntry_quantity')
        VIP_price_id = request.POST.get('VIP_price_id')
        VIP_quantity = request.POST.get('VIP_quantity')

        try:
            earlybird_cat = int(request.POST.get('EarlyBird_quantity', 0))
        except ValueError:
            earlybird_cat = 0

        try:   
            general_entry_cat = int(request.POST.get('GeneralEntry_quantity', 0))
        except ValueError:
            general_entry_cat = 0
            

        try:
            vip_cat = int(request.POST.get('VIP_quantity', 0))
        except ValueError:
            vip_cat = 0


        if earlybird_cat < 0 or general_entry_cat < 0 or vip_cat < 0:
            messages.error(request, "Va rugam sa introduceti un numar de bilete pozitiv.")
            return render(request, 'vanzareBilete/event.html', context = {'eventVariable': event})

        if earlybird_cat > 0:
            for i in range(earlybird_cat):
                ticket = Ticket.objects.create(
                    event = event,
                    owner = user,
                    price = EarlyBird_price_final,
                    category = 'Earlybird'
                )

        if general_entry_cat > 0:
            for i in range(general_entry_cat):
                ticket = Ticket.objects.create(
                    event = event,
                    owner = user,
                    price = GeneralEntry_price_final,
                    category = 'General entry'
                )

        if vip_cat > 0:
            for i in range(vip_cat):
                ticket = Ticket.objects.create(
                    event = event,
                    owner = user,
                    price = VIP_price_final,
                    category = 'VIP'
                )

        checkout_session = stripe.checkout.Session.create(
            line_items=[
                {
                    'price': EarlyBird_price_id,
                    'quantity': EarlyBird_quantity,
                },
                {
                    'price': GeneralEntry_price_id,
                    'quantity': GeneralEntry_quantity,
                },
                {
                    'price': VIP_price_id,
                    'quantity': VIP_quantity,
                }
            ],
            payment_method_types=['card'],
            mode = 'payment',
            customer_creation='always',
            success_url=f'{settings.BASE_URL}{'succesPayment/'}',
            cancel_url=f'{settings.BASE_URL}{'cancelPayment/'}',
        )
        return redirect(checkout_session.url, code=303)
    
    


    context = {
        'eventVariable': event,
        'EarlyBird_product': EarlyBird_product,
        'EarlyBird_price': EarlyBird_price,
        'EarlyBird_price_final': EarlyBird_price_final,
        'GeneralEntry_product': GeneralEntry_product,
        'GeneralEntry_price': GeneralEntry_price,
        'GeneralEntry_price_final': GeneralEntry_price_final,
        'VIP_product': VIP_product,
        'VIP_price': VIP_price,
        'VIP_price_final': VIP_price_final
    }
    return render(request, 'vanzareBilete/event.html', context)

def succesPayment(request):

    context = {}
    return render(request, 'vanzareBilete/succesPayment.html', context)

def cancelPayment(request):

    context = {}
    return render(request, 'vanzareBilete/cancelPayment.html', context)


        
