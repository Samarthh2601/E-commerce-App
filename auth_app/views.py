from django.shortcuts import render, redirect
from django.http import HttpRequest
from django.contrib import messages
from .forms import UserUpdateForm, UserSignUpForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.contrib.auth.models import User
from .models import Profile

def register(request: HttpRequest):
    if request.method == "GET":
        return render(request, 'auth_app/register.html', {'form': UserSignUpForm()})

    form = UserSignUpForm(request.POST)
    if form.is_valid():
        data = form.cleaned_data

        User.objects.create_user(username=data['username'], email=data['email'], password=data['password1'])
        
        Profile.objects.create(user=User.objects.get(username=data['username']), phone_number=data['phone_number'], address=data['address'], city=data['city'], state=data['state'], zip_code=data['zip_code'], profile_picture=data['profile_picture'])

        username = form.cleaned_data.get('username')
        messages.success(request, f'Account created for {username}!')
        return redirect('register')
    else:
        print(form.errors)
        messages.warning(request,form.errors)
        return redirect('register')

# def register(request: HttpRequest):
#     if request.method == "GET":
#         return render(request, 'auth_app/register.html', {'form': UserRegisterForm()})

#     form = UserRegisterForm(request.POST)
#     if form.is_valid():
#         form.save()
#         username = form.cleaned_data.get('username')
#         messages.success(request, f'Account created for {username}!')
#         return redirect('login')
#     else:
#         messages.warning(request,form.errors)
#         return redirect('register')

@login_required
def profile(request):
    print(request.user)
    print(request.user.__dict__)
    return render(request, 'auth_app/profile.html')

@login_required
def user_logout(request):
    logout(request)
    return render(request, 'auth_app/logout.html')