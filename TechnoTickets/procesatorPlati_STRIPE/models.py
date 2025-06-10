from django.db import models
from vanzareBilete.models import CustomUser

# Create your models here.

class UserPayment(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    stripe_customer_id = models.CharField(max_length=200)
    stripe_checkout_id = models.CharField(max_length=200)
    stripe_product_id = models.CharField(max_length=200)
    product_name = models.CharField(max_length=200)
    quantity = models.IntegerField(default=0)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    currency = models.CharField(max_length=200)
    has_paid = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.username} - {self.product.name} - Paid: {self.has_paid}"