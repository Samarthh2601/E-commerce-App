from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

class Product(models.Model):
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to='product_pics')
    price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField(max_length=500)
    stock = models.IntegerField()
    available = models.BooleanField(default=True)
    created_at = models.DateTimeField(default=timezone.now)
    seller = models.ForeignKey(User, on_delete=models.CASCADE, null=True)

