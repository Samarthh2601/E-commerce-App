from django.shortcuts import render, redirect
from django.http import HttpRequest
from django.contrib import messages
from .forms import UserRegisterForm

def register(request: HttpRequest):
    if request.method == "GET":
        return render(request, 'auth_app/register.html', {'form': UserRegisterForm()})

    form = UserRegisterForm(request.POST)
    if form.is_valid():
        form.save()
        username = form.cleaned_data.get('username')
        messages.success(request, f'Account created for {username}!')
        return redirect('login')
    else:
        messages.warning(request, 'The form you submitted was invalid. Please try again.')
        return redirect('register')