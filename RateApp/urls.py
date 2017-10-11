from django.conf.urls import url
from django.contrib.auth import views as auth_views
from . import views

app_name = 'RateApp'
urlpatterns = [
    url(r'^home/$', views.home, name='home'),
    url(r'^reg/$', views.registration, name='registration'),

]
