from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.conf import settings
from django_resized import ResizedImageField

class Product(models.Model):
    name = models.CharField(max_length=100)
    image = ResizedImageField(size=[400, 300], quality=100, upload_to='product_pics', default='product_pics/default.jpg')
    price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField(max_length=500)
    stock = models.IntegerField()
    available = models.BooleanField(default=True)
    created_at = models.DateTimeField(default=timezone.now)
    category = models.CharField(max_length=100, choices=settings.CATEGORY_CHOICES, default='General')
    seller = models.ForeignKey(User, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.name

class Wishlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    products = models.CharField(max_length=175, default=None)
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.user.username
    
    @staticmethod
    def save_product(user: User, product_key: int):
        obj = Wishlist.objects.filter(user=user)
        if not obj.exists():
            Wishlist(user=user, products=str(product_key) + ',').save()
        else:
            obj = obj.first()
            obj.products += str(product_key) + ','
        obj.save()
    
    @staticmethod
    def get_wishlist_products(user: User, obj=False) -> bool | list | list[Product]:
        objects = Wishlist.objects.filter(user=user)

        if not objects.exists():
            return False
        sp = objects.first().products.split(',')[:-1]

        if obj is False:
            return sp

        ls = [Product.objects.filter(id=key).first() for key in sp]
        return ls