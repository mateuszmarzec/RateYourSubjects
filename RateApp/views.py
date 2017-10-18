from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from . import forms
from .models import UserData, Rate, Teacher, Subject
from django.contrib import messages
from django.http import Http404
from . import encoding_functions
from . import additional_scripts



# Create your views here.

@login_required
def home(request):
    if request.method == 'POST':
        form = forms.SearchForm(request.POST)
        if form.is_valid():
            subject = form.cleaned_data['subject']
            leader = form.cleaned_data['teacher']

            return redirect('RateApp:search', subject)
    form = forms.SearchForm()
    return render(request, 'RateApp/home.html', {'form': form})

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
    user_info = additional_scripts.create_two_dem_arr(user_data, user_data_titles)
    return render(request, 'RateApp/user_info.html', {'user_info': user_info})

@login_required
def rate(request):

    subjects = Subject.objects.all().values_list('shortcut', flat=True)
    teachers = Teacher.objects.all().values_list()

    if request.method == 'POST':
        form = forms.RateForm(request.POST)
        if form.is_valid():
            subject = form.cleaned_data['subject']
            leader = form.cleaned_data['leader']
            how_interesting = form.cleaned_data['how_interesting']
            how_easy = form.cleaned_data['how_easy']
            description = form.cleaned_data['description']

            rate = Rate(how_interesting=how_interesting, how_easy=how_easy,
                        leader=Teacher.objects.get(first_name=leader),
                        description=description, subject=Subject.objects.get(name=subject),
                        user=UserData.objects.get(login=request.user.username))
            rate.save()
            return render(request, 'RateApp/rate.html', {'form': form})
    form = forms.RateForm()
    return render(request, 'RateApp/rate.html', {'form': form, 'subjects': subjects, 'teachers': teachers})

@login_required
def search(request, fraze):
    raise Http404