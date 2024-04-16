from django import forms
from django.conf import settings

class AddProduct(forms.Form):
    name = forms.CharField(max_length=100)
    image = forms.ImageField()
    price = forms.DecimalField(max_digits=10, decimal_places=2)
    description = forms.CharField(max_length=500)
    stock = forms.IntegerField()
    available = forms.BooleanField(initial=True)
    category = forms.ChoiceField(choices=settings.CATEGORY_CHOICES)