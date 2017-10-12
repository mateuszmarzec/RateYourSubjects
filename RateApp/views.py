from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from . import forms, models
from Account import models


# Create your views here.

@login_required
def home(request):
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



