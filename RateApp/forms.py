from django import forms
from . import fields, models, additional_scripts

### Account Staff
class LoginForm(forms.Form):
    login = forms.CharField(max_length=20)
    password = forms.CharField(max_length=50, widget=forms.PasswordInput())

class RegisterForm(forms.Form):
    login = forms.CharField(max_length=20)
    password = forms.CharField(max_length=50, widget=forms.PasswordInput())
    confirm_password = forms.CharField(max_length=50, widget=forms.PasswordInput())
    email = forms.EmailField()

class PasswordChangeForm(forms.Form):
    new_password = forms.CharField(widget=forms.PasswordInput)
    new_password_confirm = forms.CharField(widget=forms.PasswordInput)


### Rate Staff
class RateForm(forms.Form):
    subject = forms.CharField(required=False)
    leader = forms.CharField(required=False)
    how_interesting = forms.IntegerField(initial=50)
    how_easy = forms.IntegerField(initial=50)
    description = forms.CharField(required=False)



class SearchForm(forms.Form):
    teacher = forms.CharField(required=False)
    subject = forms.CharField(required=False)




