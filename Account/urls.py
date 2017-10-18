from django.conf.urls import url
from django.contrib.auth import views as auth_views
from . import views

app_name = 'Account'
urlpatterns = [
    url('login/$', views.login,
        {'template_name': 'Account/login.html'}, name='login'),
    url('logout/$', auth_views.logout,
        {'template_name': 'Account/logout.html'}, name='logout'),
    url(r'^reg/$', views.registration, name='registration'),
    url(r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        views.activate, name='activate'),
]
