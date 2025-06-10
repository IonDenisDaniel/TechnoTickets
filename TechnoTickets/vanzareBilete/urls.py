from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name = 'home'),
    path('events/', views.events, name = 'events'),
    path('contactUs/', views.contactUs, name = 'contactUs'),
    path('register/', views.Register, name = 'register'),
    path('login/', views.LogIn, name = 'log_in'),
    path('logout/', views.LogOut, name = 'log_out'),
    path('myAccount/', views.MyAccount, name = 'my_account'),
    path('updateUserFirstName/', views.updateUserFirstName, name = 'update_user_first_name'),
    path('updateUserLastName/', views.updateUserLastName, name = 'update_user_last_name'),
    path('updateUserEmail/', views.updateUserEmail, name = 'update_user_email'),
    path('udateUserPassword/', views.updateUserPassword, name = 'update_user_password'),
    path('updateUserProfilePicture/', views.updateUserProfilePicture, name = 'update_user_profile_picture'),
    path('eventPage/<str:primary_key>/', views.EventPage, name = 'event_page'),
    path('succesPayment/', views.succesPayment, name = 'succes_payment'),
    path('cancelPayment/', views.cancelPayment, name = 'cancel_payment')
]