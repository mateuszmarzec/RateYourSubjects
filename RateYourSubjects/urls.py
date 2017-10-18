"""RateYourSubjects URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from . import admin
from django.contrib import admin as adm
from Account import forms, views
from django.views.generic.base import RedirectView
from django.contrib.auth import views as auth_views

urlpatterns = [
    url(r'^$', RedirectView.as_view(url='/home/')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^account/', include('Account.urls')),
    url(r'^', include('RateApp.urls')),
    url(r'^password_reset/$',
        auth_views.password_reset,
        {'template_name': 'registration/password_reset_form.html', 'password_reset_form': forms.EmailValidationOnForgotPassword},
        name="password_reset"),
    url(r'^password_reset/done/$', auth_views.password_reset_done, {'template_name': 'registration/password_reset_done.html'}, name='password_reset_done'),
    url(r'^reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$', auth_views.password_reset_confirm, {'set_password_form': forms.NewPasswordSave}, name='password_reset_confirm'),
    url(r'^reset/done/$', auth_views.password_reset_complete, name='password_reset_complete'),

]
adm.autodiscover()