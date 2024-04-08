from django.shortcuts import render
from django.http import HttpRequest
from django.conf import settings

def home(request: HttpRequest):
    return render(request, 'ecomm_app/home.html', {'title': 'Home', 'categories': settings.CATEGORIES})