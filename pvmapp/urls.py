from django.urls import path
from . import views

urlpatterns = [
    path('', views.pvm_home, name='pvm_home'),
    path('mob-gen/', views.monster_generator, name='mob-gen-url'),
    path('random-mob/', views.random_mob_fight, name='random-mob-url'),
]
