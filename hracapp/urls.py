from urllib import request
from django.urls import path

from .economy import buy_or_sell, buy_or_sell_convert
from . import views
from .xp_lvl import plus_xp
from django.contrib.auth import views as auth_views
from django.contrib.auth.views import LoginView, LogoutView
from . import xp_lvl, economy, update_atributs

urlpatterns = [
    path('logout', views.custom_logout, name='logout-url'),
    path('profile', views.profile, name='profile-url'),
    path('eqp-url/<int:item_id>/', views.equip_item, name='eqp-url'),
    path('de-eqp-url/<int:item_id>/', views.dequip_item, name='de-eqp-url'),
    path('plus_xp', xp_lvl.plus_xp, name='plus_xp-url'),
    path('gold_transaction', economy.buy_or_sell_convert, name='gold_transaction-url'),
    path('atributs-update', update_atributs.atr_update, name='atributs-update-url'),
    path('sell_item/<int:item_id>/', economy.sell_item, name='sell_item-url'),
    ]