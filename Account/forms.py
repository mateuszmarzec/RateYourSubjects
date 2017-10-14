from django.contrib.auth import password_validation
from django.contrib.auth.forms import *
from django.contrib.auth.models import User
from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.shortcuts import get_current_site
from django.core.exceptions import ValidationError
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from RateApp.models import UserData
from RateApp import encoding_functions

## PasswordResetForm subclass to enable reseting password
class EmailValidationOnForgotPassword(PasswordResetForm):
    def get_users(self, email):
        """Given an email, return matching user(s) who should receive a reset.

        This allows subclasses to more easily customize the default policies
        that prevent inactive users and users with unusable passwords from
        resetting their password.
        """
        active_users = UserModel._default_manager.filter(**{
            '%s__iexact' % UserModel.get_email_field_name(): email,
            'is_active': True,
        })
        return (u for u in active_users)

## SetPasswordForm subclass to set password in database
class NewPasswordSave(SetPasswordForm):

    def save(self, commit=True):
        password = self.cleaned_data["new_password1"]
        self.user.set_password(password)

        # set password in my database
        tuple = encoding_functions.create_password_hash(password)
        db_user = UserData.objects.get(login=self.user)
        db_user.password_hash = tuple[1]
        db_user.password_salt = tuple[0]

        if commit:
            self.user.save()
            db_user.save()
        return self.user
