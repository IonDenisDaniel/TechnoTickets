from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser,Event, Ticket

# Register your models here.

class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ['email', 'nume', 'prenume', 'is_staff', 'is_superuser']
    ordering = ('email',)
    search_fields = ('email', 'nume', 'prenume')
    fieldsets = (
        (None, {'fields': ('email', 'password', 'nume', 'prenume')}),
        ('Permissions', {'fields': ('is_staff', 'is_active', 'is_superuser', 'groups', 'user_permissions')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'nume', 'prenume', 'password1', 'password2', 'is_staff', 'is_active')}
        ),
    )

admin.site.register(CustomUser, CustomUserAdmin)

admin.site.register(Event)
admin.site.register(Ticket)
