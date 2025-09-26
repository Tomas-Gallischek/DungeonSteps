from django.urls import path
from . import views

urlpatterns = [
    path('', views.pvm_home, name='pvm_home'),
    path('random-mob-fight/', views.random_mob_fight, name='random-mob-fight-url'),
]
