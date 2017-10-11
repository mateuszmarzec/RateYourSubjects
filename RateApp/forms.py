from django import forms


class LoginForm(forms.Form):
    login = forms.CharField(max_length=20)
    password = forms.CharField(max_length=50, widget=forms.PasswordInput())

class RegisterForm(forms.Form):
    login = forms.CharField(max_length=20)
    password = forms.CharField(max_length=50, widget=forms.PasswordInput())
    confirm_password = forms.CharField(max_length=50, widget=forms.PasswordInput())
    email = forms.EmailField()



