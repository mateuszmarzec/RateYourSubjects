from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_text
from django.utils.http import urlsafe_base64_decode
from Account.tokens import account_activation_token
from RateApp import forms, models, encoding_functions
from django.shortcuts import render, redirect
from django.contrib import messages
import subprocess, os

def registration(request):
    if request.method == 'POST':
        form = forms.RegisterForm(request.POST)
        if form.is_valid():
            user_login = form.cleaned_data['login']
            user_password = form.cleaned_data['password']
            user_confirm_password = form.cleaned_data['confirm_password']
            user_email = form.cleaned_data['email']
            try:
                models.UserData.objects.get(login=user_login)
                messages.error(request, 'This login is already in use', 'reg_error')
                return render(request, 'Account/registration.html', {'form': form})
            except models.UserData.DoesNotExist:
                if user_password == user_confirm_password:
                    tuple = encoding_functions.create_password_hash(user_password)
                    user = models.UserData(login=user_login, password_hash=tuple[1], password_salt=tuple[0], email=user_email)
                    user.save()
                    current_site = get_current_site(request)
                    subprocess.call(["python3 email_confirm.py"], shell=True, cwd=os.path.dirname(os.path.abspath('RateYourSubjects')))
                    messages.success(request, 'You\'re now a member of our community', 'Congratulations!')
                    messages.success(request, 'We\'ve just sent you a confirmation message', 'Check Your mail box!')
                    return redirect('Account:login')
                else:
                    messages.error(request, 'Password and Confirm Password are not the same!', 'reg_error')
                    return render(request, 'Account/registration.html', {'form': form})
        return render(request, 'Account/registration.html', {'form': form})
    else:
        form = forms.RegisterForm()
        return render(request, 'Account/registration.html', {'form': form})

def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = models.UserData.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, models.UserData.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        # return redirect('home')
        return render(request, 'Account/registration_confirm.html')
    else:
        return render(request, 'Account/registration_fail.html')
