from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from . import forms, models


# Create your views here.

@login_required
def home(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            form = forms.LoginForm(request.POST)
            if form.is_valid():
                user_login = form.cleaned_data['login']
                user_password = form.cleaned_data['password']
                if login_success(user_login=user_login, password=user_password):
                    print("Gratuluej")
                    request.user = user_login
                    print(request.user)
                else:
                    print("CHujowo")
            return render(request, 'RateApp/login.html', {'form': form})
        else:
            form = forms.LoginForm()
            return render(request, 'RateApp/login.html', {'form': form})
    else:
        return render(request, 'RateApp/registration.html')

@login_required
def registration(request):
    if request.method == 'POST':
        form = forms.RegisterForm(request.POST)
        if form.is_valid():
            user_login = form.cleaned_data['login']
            user_password = form.cleaned_data['password']
            user_confirm_password = form.cleaned_data['confirm_password']
            user_email = form.cleaned_data['email']
        return render(request, 'RateApp/registration.html', {'form': form})
    else:
        form = forms.RegisterForm()
        return render(request, 'RateApp/registration.html', {'form': form})

