from typing import final
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
    hp = Atributs.objects.get(hrac=user).suma_hp


    p_deffence = player_deffence(request)
    player_hp = p_deffence['player_hp']
    kolo = 1

    while player_hp >= 0:

        print(f"Kolo souboje: {kolo}")

        p_attack = player_attack(request)
        attack_value = p_attack['final_attack']
        attack_status = p_attack['attack_status']
        attack_type = p_attack['attack_type']

        p_deffence = player_deffence(request)
        armor_normal = p_deffence['armor_normal']
        armor_light = p_deffence['armor_light']
        armor_heavy = p_deffence['armor_heavy']
        armor_magic = p_deffence['armor_magic']

        if attack_type == "universal":
            defence = armor_normal
        elif attack_type == "light":
            defence = armor_light
        elif attack_type == "heavy":
            defence = armor_heavy
        elif attack_type == "magic":
            defence = armor_magic

        damage_taken = round(attack_value - defence)

        if damage_taken < 0:
            damage_taken = 0
            miss = True
        else:
            miss = False
            hp_before = player_hp
            player_hp -= damage_taken
            hp_after = player_hp
            hp_minus = hp_before - hp_after
            kolo += 1

        print(f"MISS STATUS: {miss}, {damage_taken} poškození")
        print(f"Útok byl {attack_value} a byl {attack_status} ({attack_type}). Soupeř se bránil hodnotou {defence} a hráčovi zbývá {player_hp} HP. Ubráno bylo {hp_minus} HP.")

    context = {
        'user': user,

    }
    return render(request, 'pvmapp/pvm_home.html', context)





