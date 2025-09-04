from urllib import request
from django.urls import path
from . import views
from .xp_lvl import plus_xp
from django.contrib.auth import views as auth_views
from django.contrib.auth.views import LoginView, LogoutView
from . import xp_lvl

urlpatterns = [
    path('logout', views.custom_logout, name='logout-url'),
    path('profile', views.profile, name='profile-url'),
    path('gold_per_second', views.gold_per_second, name='views-data-url'),  
    path('upgrade-attribute/', views.update_attribute, name='upgrade-attribute-url'),
    path('eqp-url/<int:item_id>/', views.equip_item, name='eqp-url'),
    path('de-eqp-url/<int:item_id>/', views.dequip_item, name='de-eqp-url'),
    path('plus_xp', xp_lvl.plus_xp, name='plus_xp-url'),
    ]