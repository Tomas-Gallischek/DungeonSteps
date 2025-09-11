from django.contrib.auth import logout
from django.shortcuts import redirect, render
from django.urls import reverse
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from hracapp. models import EQP, INV, XP_LVL, Character_bonus, Economy, Atributs


@login_required
def pvm_home(request):
    user = request.user
    player_info = player_info_funkce(request)

    print(player_info)

    context = {
        'user': user,
        'player_info': player_info,
    }
    return render(request, 'pvmapp/pvm_home.html', context)





def player_info_funkce(request):
    user = request.user
    character_bonus = Character_bonus.objects.filter(hrac=user).first()
    atributs = Atributs.objects.filter(hrac=user).first()
    eqp = EQP.objects.filter(hrac=user).first()
    xp_lvl = XP_LVL.objects.filter(hrac=user).first()

    context = {
        'user': user,
        'character_bonus': character_bonus,
        'atributs': atributs,
        'eqp': eqp,
        'xp_lvl': xp_lvl,
    }
    return context