from RateApp import forms
from django.shortcuts import render

def registration(request):
    print("sada")
    if request.method == 'POSTT':
        form = forms.RegisterForm(request.POST)
        user_login = form.cleaned_data['login']
        if form.is_valid():
            user_login = form.cleaned_data['login']
            user_password = form.cleaned_data['password']
            user_confirm_password = form.cleaned_data['confirm_password']
            user_email = form.cleaned_data['email']
        return render(request, 'RateApp/registration.html', {'form': form})
    else:
        form = forms.RegisterForm()
        return render(request, 'Account/login.html', {'form': form})