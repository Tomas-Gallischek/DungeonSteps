from django.urls import path
from . import views

urlpatterns = [
    path('', views.shop, name='shop-url'),
    path('reset/', views.shop_reset, name='shop-reset-url'),

    ]