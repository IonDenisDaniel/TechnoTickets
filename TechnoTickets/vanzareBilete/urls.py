from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name = 'home'),
    path('events/', views.events, name = 'events'),
    path('contactUs/', views.contactUs, name = 'contactUs'),
    path('register/', views.Register, name = 'register'),
    path('login/', views.LogIn, name = 'log_in'),
    path('logout/', views.LogOut, name = 'log_out'),
    path('myAccount/', views.MyAccount, name = 'my_account')
]