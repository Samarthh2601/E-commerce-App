from django.shortcuts import render, redirect
from django.http import HttpRequest
from django.conf import settings
from .models import Product, Inventory
from .forms import AddProduct
from django.contrib import messages
from django.contrib.auth.decorators import login_required


def home(request: HttpRequest):
    return render(request, 'ecomm_app/product_list.html', {'title': 'Home', 'categories': settings.CATEGORIES, 'products': reversed(Product.objects.all())})

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
    
@login_required
def product_detail(request: HttpRequest, product_id: int):
    product = Product.objects.get(id=product_id)
    return render(request, 'ecomm_app/product_detail.html', {'title': product.name, 'product': product, 'categories': settings.CATEGORIES})

@login_required
def add_to_wishlist(request: HttpRequest):
    if request.method == "POST":
        product_id = request.POST.get('product_id')
        Inventory.save_product(request.user, product_id, wishlist=True)
        messages.success(request, 'Product added to wishlist!')
        return redirect('home')

@login_required
def buy_now(request: HttpRequest):
    if request.method == "POST":
        product_id = request.POST.get('product_id')
        print(product_id)
        product = Product.objects.get(id=product_id)
        if product.stock > 0:
            product.stock -= 1
            product.save()
            Inventory.save_product(request.user, product_id)
            messages.success(request, 'Product bought successfully!')
        else:
            messages.warning(request, 'Product out of stock!')
        return redirect('home')

@login_required
def remove_from_wishlist(request: HttpRequest):
    if request.method == "POST":
        product_id = request.POST.get('product_id')
        if Inventory.remove_product(request.user, product_id):
            messages.success(request, 'Product removed from wishlist!')
            return redirect('wishlist')
        else:
            messages.warning(request, 'Product not found in wishlist!')
            return redirect('home')

@login_required
def wishlist(request: HttpRequest):
    return render(request, 'ecomm_app/wishlist.html', {'title': 'Wishlist', 'products': Inventory.get_products(request.user, obj=True, wishlist=True), 'categories': settings.CATEGORIES})

@login_required
def my_products(request: HttpRequest):
    return render(request, 'ecomm_app/product_list.html', {'title': 'My Products', 'products': Product.objects.filter(seller=request.user), 'categories': settings.CATEGORIES})

@login_required
def bought_products(request: HttpRequest):
    products = Inventory.get_products(request.user, obj=True)
    return render(request, 'ecomm_app/product_list.html', {'title': 'My Products', 'products': products, 'categories': settings.CATEGORIES})
