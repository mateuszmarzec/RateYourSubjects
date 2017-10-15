from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from . import forms
from .models import UserData
from django.contrib import messages
from django.http import Http404
from . import encoding_functions



# Create your views here.

@login_required
def home(request):
    return render(request, 'RateApp/home.html')

@login_required
def password_change(request):
    if request.method == 'POST':
        form = forms.PasswordChangeForm(request.POST)
        if form.is_valid():
            try:
                # get user from db's
                db_user = UserData.objects.get(login=request.user.username)

                # get password from form
                password = form.cleaned_data['new_password']
                password_confirm = form.cleaned_data['new_password_confirm']

                # check if password are the same
                if password != password_confirm:
                    messages.error(request, 'Passwords are not the same')
                    return render(request, 'RateApp/password_change.html', {'form': form})

                # create password hash
                tuple = encoding_functions.create_password_hash(password)

                # change password
                db_user.password_hash = tuple[1]
                db_user.password_salt = tuple[0]
                db_user.save()

                messages.success(request, 'Password changed', 'It works!')
                return redirect('RateApp:home')
            except:
                raise Http404
        return render(request, 'RateApp/password_change.html', {'form': form})
    form = forms.PasswordChangeForm()
    return render(request, 'RateApp/password_change.html', {'form': form})


@login_required
def user_info(request):
    user = UserData.objects.get(login=request.user.username)
    user_data = [user.login, user.email, user.last_login, user.is_active, user.registration_date]
    user_data_titles = ['Login', 'Email', 'Last Login', 'Is Active', 'Registration Date']

    # creating matrix used to show user info
    user_info = [[0 for x in range(2)] for y in range(len(user_data))]
    i = 0
    for users in user_info:
        users[1] = user_data[i]
        users[0] = user_data_titles[i]
        i = i + 1

    return render(request, 'RateApp/user_info.html', {'user': user_info})
