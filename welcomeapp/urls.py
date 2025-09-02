from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from django.contrib.auth.views import LoginView, LogoutView


urlpatterns = [
    path('', views.index, name='index'),
    path('register', views.register, name='register-url'),
    path('login', auth_views.LoginView.as_view(template_name='welcomeapp/login.html'), name='login-url'),
    ]