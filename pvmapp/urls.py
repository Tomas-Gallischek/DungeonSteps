from django.urls import path
from . import views

urlpatterns = [
    path('', views.pvm_home, name='pvm_home'),
    path('random-mob-fight/', views.random_mob_fight, name='random-mob-fight-url'),
    path('dungeon-mob-fight/', views.dungeon_mob_fight, name='dungeon-mob-fight-url'),
    path('dungeon-map/', views.dungeon_map_all, name='dungeon_map-url'),
    path('map-base-camp/', views.dungeon_map_chosen, name='map-base-camp-url'),
]
