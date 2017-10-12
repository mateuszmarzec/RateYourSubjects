from RateApp import forms
from django.shortcuts import render, redirect
from django.contrib import messages

def registration(request):
    if request.method == 'POST':
        form = forms.RegisterForm(request.POST)
        if form.is_valid():
            user_login = form.cleaned_data['login']
            user_password = form.cleaned_data['password']
            user_confirm_password = form.cleaned_data['confirm_password']
            user_email = form.cleaned_data['email']
            print(user_password)
            messages.success(request, 'You\'re now a member of our community', 'Congratulations!')
            return redirect('Account:login')
        return render(request, 'Account/registration.html', {'form': form})
    else:
        form = forms.RegisterForm()
        return render(request, 'Account/registration.html', {'form': form})
