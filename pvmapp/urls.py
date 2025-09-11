from django.urls import path
from . import views

urlpatterns = [
    path('', views.pvm_home, name='pvm_home'),
]
