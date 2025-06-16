import uuid
from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, PermissionsMixin

from django.conf import settings

# Create your models here.

class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        email = self.normalize_email(email)
        
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)

        return user
    
    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        return self.create_user(email, password, **extra_fields)
    


class CustomUser(AbstractBaseUser, PermissionsMixin):
    nume = models.CharField(max_length=200)
    prenume = models.CharField(max_length=200)
    email = models.EmailField(unique=True)
    profile_image = models.ImageField(null=True, blank=True)

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email


class Event(models.Model):
    denumire = models.CharField(max_length=200)
    location = models.CharField(max_length=200)
    data = models.DateField()
    ora_incepere = models.TimeField()
    ora_terminare = models.TimeField()
    descriere = models.CharField(max_length=500)
    image = models.ImageField(upload_to='event_images/', blank=True)
    colorTheme = models.CharField(max_length=100, null=True, blank=True)
    latitudine = models.FloatField(null=True)
    longitudine = models.FloatField(null=True)


    def __str__(self):
        return self.denumire
    
class Ticket(models.Model):
    CATEGORY = (
        ('Earlybird', 'Earlybird'),
        ('General entry', 'General entry'),
        ('VIP', 'VIP')
    )
    id = models.UUIDField(primary_key=True, default = uuid.uuid4, editable=False)
    event = models.ForeignKey('Event', on_delete=models.CASCADE)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    purchase_date = models.DateField(auto_now_add=True)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    category = models.CharField(max_length=200, null = True, choices=CATEGORY)

    def __str__(self):
        return f"Bilet: {self.id} pentru eveniment: {self.event} - owner: {self.owner}"

class QRCode(models.Model):

    id = models.UUIDField(primary_key=True, default = uuid.uuid4, editable=False)
    token = models.CharField(max_length=64, unique=True)
    is_used = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.token

class QRScan(models.Model):

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    qr = models.ForeignKey(QRCode, on_delete=models.CASCADE)
    scanned_at = models.DateTimeField(auto_now_add=True)
    is_used = models.BooleanField(default=True)

    class Meta:
        unique_together = ('user', 'qr')

    def __str__(self):
        return f"{self.user.nume} {self.user.prenume}: {self.qr.token}"