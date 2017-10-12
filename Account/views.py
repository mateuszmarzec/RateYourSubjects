from RateApp import forms, models, encoding_functions
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
            try:
                models.UserData.objects.get(login=user_login)
                messages.error(request, 'This login is already in use', 'reg_error')
                return render(request, 'Account/registration.html', {'form': form})
            except models.UserData.DoesNotExist:
                if user_password == user_confirm_password:
                    tuple = encoding_functions.create_password_hash(user_password)
                    user = models.UserData(login=user_login, password_hash=tuple[1], password_salt=tuple[0], email=user_email)
                    user.save()
                    messages.success(request, 'You\'re now a member of our community', 'Congratulations!')
                    return redirect('Account:login')
                else:
                    messages.error(request, 'Password and Confirm Password are not the same!', 'reg_error')
                    return render(request, 'Account/registration.html', {'form': form})
        return render(request, 'Account/registration.html', {'form': form})
    else:
        form = forms.RegisterForm()
        return render(request, 'Account/registration.html', {'form': form})
