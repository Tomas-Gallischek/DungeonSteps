from django.contrib.auth import logout
from django.shortcuts import redirect, render
from django.urls import reverse
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from hracapp. models import EQP, INV, XP_LVL, Character_bonus, Economy, Atributs
from .player_off_def import player_attack, player_deffence


@login_required
def pvm_home(request):
    user = request.user


    attack = player_attack(request)
    deffence = player_deffence(request)


    context = {
        'user': user,
        'attack': attack,
        'deffence': deffence,
    }
    return render(request, 'pvmapp/pvm_home.html', context)





