from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
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

            if leader == '':
                return redirect('RateApp:search_subject', subject)
            else:
                return redirect('RateApp:search_teacher', leader)

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

            teacher = leader.split()

            rate = Rate(how_interesting=how_interesting, how_easy=how_easy,
                        leader=Teacher.objects.get(first_name=teacher[0], last_name=teacher[1]),
                        description=description, subject=Subject.objects.get(shortcut=subject),
                        user=UserData.objects.get(login=request.user.username))
            rate.save()

            subject = Subject.objects.get(shortcut=subject)
            subject.leaders.add(Teacher.objects.get(first_name=teacher[0], last_name=teacher[1]))
            subject.save()

            messages.success(request, 'Rate added successfully!', 'Success')
            return redirect('RateApp:home')
    form = forms.RateForm()
    return render(request, 'RateApp/rate.html', {'form': form, 'subjects': subjects, 'teachers': teachers})

@login_required
def search_subject(request, fraze):
    #rates = Rate.objects.filter(subject = get_object_or_404(Subject, shortcut=fraze))
    subject = get_object_or_404(Subject, shortcut=fraze)
    averange = additional_scripts.get_average(id=subject.id, type='subject')
    teachers = Teacher.objects.filter(subject=subject).values_list()
    return render(request, 'RateApp/search_subject.html', {'subject': subject, 'av': averange, 'teachers': teachers})

@login_required
def search_teacher(request, fraze):
    #rates = Rate.objects.filter(leader = get_object_or_404(Teacher, last_name=fraze))
    teacher = get_object_or_404(Teacher, last_name=fraze)
    averange = additional_scripts.get_average(id=teacher.id, type='teacher')
    subjects = Subject.objects.filter(leaders=teacher).values_list()
    return render(request, 'RateApp/search_teacher.html', {'subjects': subjects, 'av': averange, 'teacher': teacher})

@login_required
def subject_details(request, shortcut):
    #rates = Rate.objects.filter(subject = get_object_or_404(Subject, shortcut=fraze))
    subject = get_object_or_404(Subject, shortcut=shortcut)
    rates = Rate.objects.filter(subject=subject)
    return render(request, 'RateApp/subject_details.html', {'rates': rates, 'subject':subject.name})

@login_required
def teacher_details(request, id):
    #rates = Rate.objects.filter(subject = get_object_or_404(Subject, shortcut=fraze))
    teacher = get_object_or_404(Teacher, pk=id)
    rates = Rate.objects.filter(leader=teacher)
    teacher_name = teacher.first_name + " " + teacher.last_name
    return render(request, 'RateApp/teacher_details.html', {'rates': rates, 'teacher': teacher_name})