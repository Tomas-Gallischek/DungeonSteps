from django.urls import path
from . import views

urlpatterns = [
    path('', views.shop, name='shop-url'),
    path('reset/', views.shop_reset, name='shop-reset-url'),
    path('buy/<int:item_id>/', views.shop_buy, name='shop-buy-url'),

    ]