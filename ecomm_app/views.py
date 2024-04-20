from django.shortcuts import render, redirect
from django.http import HttpRequest
from django.conf import settings
from .models import Product, Wishlist
from .forms import AddProduct
from django.contrib import messages
from django.contrib.auth.decorators import login_required


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
    
def product_detail(request: HttpRequest, product_id: int):
    product = Product.objects.get(id=product_id)
    return render(request, 'ecomm_app/product_detail.html', {'title': product.name, 'product': product})

@login_required
def add_to_wishlist(request: HttpRequest):
    if request.method == "POST":
        product_id = request.POST.get('product_id')
        Wishlist.save_product(request.user, product_id)
        messages.success(request, 'Product added to wishlist!')
        return redirect('home')
    
@login_required
def wishlist(request: HttpRequest):
    ps = Wishlist.get_wishlist_products(request.user, obj=True)
    print(ps)
    return render(request, 'ecomm_app/wishlist.html', {'title': 'Wishlist', 'products': Wishlist.get_wishlist_products(request.user, obj=True)})