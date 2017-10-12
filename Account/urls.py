from django.conf.urls import url
from django.contrib.auth import views as auth_views
from . import views

app_name = 'Account'
urlpatterns = [
    url('login/$', auth_views.login,
        {'template_name': 'Account/login.html'}, name='login'),
    url('logout/$', auth_views.logout,
        {'template_name': 'Account/logout.html'}, name='logout'),

]
