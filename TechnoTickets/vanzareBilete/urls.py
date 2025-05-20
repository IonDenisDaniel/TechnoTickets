from django.urls import path
from . import views

urlpatterns = [
    path('', views.home),
    path('events/', views.events),
    path('contactUs/', views.contactUs)
]