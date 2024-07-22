from django.shortcuts import render, redirect
from django.http import HttpRequest
from django.conf import settings
from .models import Product, Inventory
from .forms import AddUpdateProduct
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

# <---------------------------------- Home ---------------------------------->

def home(request: HttpRequest):
    return render(request, 'ecomm_app/product_list.html', {'title': 'Home', 'categories': settings.CATEGORIES, 'products': reversed(Product.objects.all())})

# <---------------------------------- Product ---------------------------------->

def add_product(request: HttpRequest):
    if request.method == 'GET':
        return render(request, 'ecomm_app/add_product.html', {'title': 'Create Product', 'form': AddUpdateProduct(), 'categories': settings.CATEGORIES})
        
    else:
        form = AddUpdateProduct(request.POST, request.FILES)
        if form.is_valid():
            product = Product(name=form.cleaned_data['name'], image=form.cleaned_data['image'], price=form.cleaned_data['price'], description=form.cleaned_data['description'], stock=form.cleaned_data['stock'], available=form.cleaned_data['available'], category=form.cleaned_data['category'], seller=request.user)
            product.save()
            messages.success(request, 'Product added successfully!')
            return redirect('home')
        messages.warning(request, 'Invalid form data!')
        return render(request, 'ecomm_app/add_product.html', {'title': 'Create Product', 'form': form, 'categories': settings.CATEGORIES})

def update_product(request: HttpRequest, product_id: int):
    product = Product.objects.get(id=product_id)
    if product.seller != request.user:
        messages.warning(request, 'You are not authorized to update this product!')
        return redirect('home')
    if request.method == 'GET':
        form = AddUpdateProduct(instance=product)
        return render(request, 'ecomm_app/update_product.html', {'title': 'Update Product', 'form': form, 'product': product, 'categories': settings.CATEGORIES})

    elif request.method == 'POST':
        form = AddUpdateProduct(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            messages.success(request, 'Product updated successfully!')
            return redirect('product_detail', product_id=product_id)
        messages.warning(request, 'Invalid form data!')
        return render(request, 'ecomm_app/update_product.html', {'title': 'Update Product', 'form': form, 'product': product, 'categories': settings.CATEGORIES})

@login_required
def product_detail(request: HttpRequest, product_id: int):
    product = Product.objects.get(id=product_id)
    return render(request, 'ecomm_app/product_detail.html', {'title': product.name, 'product': product, 'categories': settings.CATEGORIES, 'seller': product.seller})

@login_required
def my_products(request: HttpRequest):
    return render(request, 'ecomm_app/product_list.html', {'title': 'My Products', 'products': Product.objects.filter(seller=request.user), 'categories': settings.CATEGORIES})

@login_required
def bought_products(request: HttpRequest):
    products = Inventory.get_products(request.user, obj=True)
    return render(request, 'ecomm_app/product_list.html', {'title': 'My Products', 'products': products, 'categories': settings.CATEGORIES})


@login_required
def buy_now(request: HttpRequest):
    if request.method == "POST":
        product_id = request.POST.get('product_id')
        product = Product.objects.get(id=product_id)
        if product.seller == request.user:
            messages.warning(request, 'You cannot buy your own product!')
            return redirect('home')
        if product.stock > 0:
            product.stock -= 1
            product.save()
            Inventory.save_product(request.user, product_id)
            messages.success(request, 'Product bought successfully!')
        else:
            messages.warning(request, 'Product out of stock!')
        return redirect('home')


def category_page(request: HttpRequest, category: str):
    return render(request, 'ecomm_app/product_list.html', {'title': f'{category.capitalize()} Category', 'categories': settings.CATEGORIES, 'products': Product.objects.filter(category=category.capitalize())})


@login_required
def remove_listed_product(request: HttpRequest):
    if request.method == "POST":
        product_id = request.POST.get('product_id')
        product = Product.objects.get(id=product_id)
        if product.seller != request.user:
            messages.warning(request, 'You are not authorized to delete this product!')
            return redirect('home')
        product.delete()
        messages.success(request, 'Product deleted successfully!')
        return redirect('my_products')

# <---------------------------------- Seller ---------------------------------->

@login_required
def seller_info(request: HttpRequest, seller_id: int):
    seller = User.objects.get(pk=seller_id)
    return render(request, 'ecomm_app/seller_info.html', {'title': 'Seller Info', 'seller': seller, 'categories': settings.CATEGORIES})

# <---------------------------------- Wishlist ---------------------------------->

@login_required
def wishlist(request: HttpRequest):
    return render(request, 'ecomm_app/wishlist.html', {'title': 'Wishlist', 'products': Inventory.get_products(request.user, obj=True, wishlist=True), 'categories': settings.CATEGORIES})

@login_required
def add_to_wishlist(request: HttpRequest):
    if request.method == "POST":
        product_id = request.POST.get('product_id')
        Inventory.save_product(request.user, product_id, wishlist=True)
        messages.success(request, 'Product added to wishlist!')
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

