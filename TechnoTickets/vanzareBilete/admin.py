from django.contrib import admin
from .models import CustomUser,Event, Ticket

# Register your models here.

admin.site.register(CustomUser)
admin.site.register(Event)
admin.site.register(Ticket)
