from django.conf import settings
from django.contrib.auth.hashers import check_password
from django.contrib.auth.models import User
from RateApp.models import *
from RateApp import encoding_functions
from datetime import datetime


class SettingsBackend(object):
    """
    Authenticate against the settings ADMIN_LOGIN and ADMIN_PASSWORD.

    Use the login name and a hash of the password. For example:

    ADMIN_LOGIN = 'admin'
    ADMIN_PASSWORD = 'pbkdf2_sha256$30000$Vo0VlMnkR4Bk$qEvtdyZRWTcOsCnI/oQ7fVOu1XAURIZYoOZ3iq8Dr4M='
    """

    def authenticate(self, request, username=None, password=None):
        if login_success(user_login=username, password=password):
            try:
                user = User.objects.get(username=username)
                user_data = UserData.objects.get(login=username)
                user_data.last_login = datetime.now()
                user_data.save()
            except User.DoesNotExist:
                user = User(username=username,
                            password=UserData.objects.values_list('password_hash', flat=True).get(login=username))
                user.save()
            return user
        return None

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None


def login_success(user_login, password):
    try:
        password_from_db_hash = UserData.objects.values_list('password_hash', flat=True).get(login=user_login)
        password_from_db_salt = UserData.objects.values_list('password_salt', flat=True).get(login=user_login)
        if UserData.objects.filter(login=user_login).exists() and encoding_functions.check_password(
                password_from_db_salt,
                password_from_db_hash, password) and UserData.objects.get(login=user_login).is_active == True:
            return True
        else:
            return False
    except UserData.DoesNotExist:
        return None
