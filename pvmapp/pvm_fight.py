import random
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Mobs
from .mobs_off_def import mob_attack, mob_deffence, mob_info
from .player_off_def import player_attack, player_deffence


def pvm_fight_funkce(request):
    user = request.user
    all_mobs = Mobs.objects.all()
    mob = random.choice(all_mobs)
    print(f"Začíná souboj mezi hráčem {user} a příšerou {mob.name}")


    # NA KONCI ULOŽIT DO FIGHT:LOG CELOU DATABÁZI SOUBOJE (fight log musí být na úrovní hráče)

