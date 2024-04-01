from django.shortcuts import render
from django.http import HttpRequest

def home(request: HttpRequest):
    # return render(request, 'ecomm_app/home.html')
    return render(request, 'ecomm_app/base.html', {'title': 'Home'})