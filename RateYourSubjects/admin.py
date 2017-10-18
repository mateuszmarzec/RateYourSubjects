from django.contrib import admin
from django.contrib.auth.forms import AuthenticationForm

class Admin(admin.AdminSite):
    def has_permission(self, request):
        return True
    pass

site = Admin()