from django.db import models
from django.utils import timezone
from auth_app.models import EUser

class Product(models.Model):
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField(max_length=500)
    stock = models.IntegerField()
    available = models.BooleanField(default=True)
    created_at = models.DateTimeField(default=timezone.now)
    seller = models.ForeignKey(EUser, on_delete=models.CASCADE, null=True)

