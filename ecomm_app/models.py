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
    
class Inventory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    wishlist_products = models.CharField(max_length=175, null=True)
    bought_products = models.CharField(max_length=1000, null=True)
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.user.username
    
    @staticmethod
    def save_product(user: User, product_key: int, *, wishlist=False) -> bool:
        obj = Inventory.objects.filter(user=user)
        if wishlist is True:
            if not obj.exists():
                Inventory(user=user, wishlist_products=str(product_key) + ',').save()
            else:
                obj = obj.first()
                obj.wishlist_products += str(product_key) + ','
                obj.save()
            return True
        
        if not obj.exists():
            Inventory(user=user, bought_products=str(product_key) + ',').save()
        else:
            obj = obj.first()
            if obj.bought_products is None:
                obj.bought_products = str(product_key) + ','
            else: obj.bought_products += str(product_key) + ','
            obj.save()
        return True

    @staticmethod
    def get_products(user: User, obj=False, *, wishlist=False) -> bool | list | list[Product]:
        objects = Inventory.objects.filter(user=user)

        if not objects.exists():
            return False
        if wishlist is True:
            field = objects.first().wishlist_products
        else:
            field = objects.first().bought_products
        if field is None:
            return False
        sp = field.split(',')[:-1]

        if obj is False:
            return sp

        ls = [Product.objects.filter(id=key).first() for key in sp]
        return ls
    
    @staticmethod
    def remove_product(user: User, product_key: int) -> bool:
        obj = Inventory.objects.filter(user=user)
        if obj.exists():
            obj = obj.first()
            products = obj.wishlist_products.split(',')
            if str(product_key) in products:
                products.remove(str(product_key))
                obj.wishlist_products = ','.join(products)
                obj.save()
                return True
        else:
            return False