from django.shortcuts import render, redirect
from django.http import HttpRequest
from django.conf import settings
from .models import Product
from .forms import AddProduct
from django.contrib import messages


def home(request: HttpRequest):
    return render(request, 'ecomm_app/home.html', {'title': 'Home', 'categories': settings.CATEGORIES, 'products': reversed(Product.objects.all())})

def add_product(request: HttpRequest):
    if request.method == 'GET':
        return render(request, 'ecomm_app/add_product.html', {'title': 'Create Product', 'form': AddProduct(), 'categories': settings.CATEGORIES})
        
    else:
        form = AddProduct(request.POST, request.FILES)
        if form.is_valid():
            product = Product(name=form.cleaned_data['name'], image=form.cleaned_data['image'], price=form.cleaned_data['price'], description=form.cleaned_data['description'], stock=form.cleaned_data['stock'], available=form.cleaned_data['available'], category=form.cleaned_data['category'], seller=request.user)
            product.save()
            messages.success(request, 'Product added successfully!')
            return redirect('home')
        messages.warning(request, 'Invalid form data!')
        return render(request, 'ecomm_app/add_product.html', {'title': 'Create Product', 'form': form, 'categories': settings.CATEGORIES})