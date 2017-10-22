from django.conf.urls import url
from django.contrib.auth import views as auth_views
from . import views

app_name = 'RateApp'
urlpatterns = [
    url(r'^home/$', views.home, name='home'),
    url(r'^user/password_change/$', views.password_change, name='password_change'),
    url(r'^user/user_info$', views.user_info, name='user_info'),
    url(r'^user/rate$', views.rate, name='rate'),
    url(r'^home/search_subject/(?P<fraze>\w+)$', views.search_subject, name='search_subject'),
    url(r'^home/search_teacher/(?P<fraze>\w+)$', views.search_teacher, name='search_teacher'),


]
