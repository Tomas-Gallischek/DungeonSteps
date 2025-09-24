from typing import final
from django.contrib.auth import logout
from django.shortcuts import redirect, render
from django.urls import reverse
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from hracapp. models import EQP, INV, XP_LVL, Character_bonus, Economy, Atributs, FightLogEntry, Fight
from .player_off_def import player_attack, player_deffence
from .mob_generator import mob_gen
from .pvm_fight import pvm_fight_funkce
import uuid

def monster_generator(request):
    mob = mob_gen(request)
    return render(request, 'pvmapp/pvm_home.html', {'mob': mob})

def random_mob_fight(request):

    fight_uuid = pvm_fight_funkce(request)
    fight_log_entries = FightLogEntry.objects.filter(fight_id=fight_uuid).order_by('timestamp')
    if fight_log_entries:
        winner_name = Fight.objects.filter(fight_id=fight_uuid).first().winner

    # + IMPORTOVAT INFORMACE O MOBCE A O HRÁČI, V SOUBOJI JE ČISTĚ SOUBOJ

    return render(request, 'pvmapp/random_mob_arena.html', {'fight_uuid': fight_uuid, 'winner_name': winner_name, 'fight_log_entries': fight_log_entries})






@login_required
def pvm_home(request):
    user = request.user

    context = {
        'user': user,

    }
    return render(request, 'pvmapp/pvm_home.html', context)





