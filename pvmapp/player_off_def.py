from pickle import NONE
import random
from typing import final
from unicodedata import category
from hracapp.models import Character_bonus, Atributs, EQP, Economy, INV, XP_LVL
from django.contrib.auth.decorators import login_required

@login_required
def player_attack(request):
    user = request.user
    lvl = XP_LVL.objects.get(hrac=user).lvl

# IMPORT ATRIBUTŮ
    player_atributs = Atributs.objects.get(hrac=user)
    player_str = player_atributs.suma_strength
    player_dex = player_atributs.suma_dexterity
    player_int = player_atributs.suma_intelligence
    player_vit = player_atributs.suma_vitality
    player_luck = player_atributs.suma_luck
    dmg_atribut_name = player_atributs.dmg_atribut
    if dmg_atribut_name == 'strength':
        dmg_atribut_value = player_str
    elif dmg_atribut_name == 'dexterity':
        dmg_atribut_value = player_dex
    elif dmg_atribut_name == 'intelligence':
        dmg_atribut_value = player_int
    else:
        dmg_atribut_value = 1
    crit_chance = (player_luck * 5) / lvl
    if crit_chance > 50:
        crit_chance = 50

# OFF BONUSY:
    player_bonus = Character_bonus.objects.get(hrac=user)
    crit_dmg_bonus = (player_bonus.kriticke_poskozeni_procenta_it_bonus /100 )
    poskozeni_utokem = 1 + (player_bonus.poskozeni_utokem_procenta_it_bonus / 100)
    pvm_bonus = 1 + (player_bonus.pvm_poskozeni_procenta_it_bonus / 100) # < ZMĚNIT AŽ BUDU IMPLMENTOVAT PVP

    # pvp_bonus = 
    # sance_na_bezvedomi_procenta_it_bonus = 
    # sance_na_otupeni_procenta_it_bonus = 
    # poskozeni_schopnosti_procenta_it_bonus = 
    # + implmentace kouzel

# IMPORT EQP
    player_eqp = EQP.objects.filter(hrac=user)
    player_weapon = player_eqp.filter(item_category='weapon').first() or None
    #více nepotřebuju, protože bonusy jsou automaticky v "character_bonus"

# VÝPOČET ÚTOKU
    if player_weapon is None:
        weapon_dmg = 2
    else:
        weapon_dmg = random.randint(player_weapon.min_dmg, player_weapon.max_dmg)
    atr_dmg = dmg_atribut_value / 10




    final_attack = round((weapon_dmg * atr_dmg) * poskozeni_utokem) * pvm_bonus
    attack_status = "normální zásah"
    attack_type = player_weapon.item_type if player_weapon else NONE


    if random.randint(1, 100) <= crit_chance:
        final_attack = round(final_attack * (2 + crit_dmg_bonus))
        attack_status = "kritický zásah"


    if final_attack <= 20:
        final_attack = random.randint(40, 80)
        attack_status = "normální zásah"

    p_attack = {
        'final_attack': final_attack,
        'attack_status': attack_status,
        'attack_type': attack_type,
    }

    return p_attack


@login_required
def player_deffence(request):
    user = request.user
    lvl = XP_LVL.objects.get(hrac=user).lvl

# IMPORT ATRIBUTŮ
    player_atributs = Atributs.objects.get(hrac=user)
    player_str = player_atributs.suma_strength
    player_dex = player_atributs.suma_dexterity
    player_int = player_atributs.suma_intelligence
    player_vit = player_atributs.suma_vitality
    player_luck = player_atributs.suma_luck

# DEF BONUSY:
    player_bonus = Character_bonus.objects.get(hrac=user)
    light_resist = 1 + (player_bonus.suma_light_resist / 100)
    heavy_resist = 1 + (player_bonus.suma_heavy_resist / 100)
    magic_resist = 1 + (player_bonus.suma_magic_resist / 100)
    pvm_resist = 1 + (player_bonus.pvm_resist_procent_it_bonus / 100) # < ZMĚNIT AŽ BUDU IMPLMENTOVAT PVP
    # pvp_resist =
    # otrava_resist_procenta_it_bonus = 
    # bezvedomi_resist_procenta_it_bonus = 


# IMPORT EQP NENÍ POTŘEBA, PROTOŽE ARMOR SI BERU Z BONUSŮ
    if player_bonus.armor_suma is None:
        armor = 1
    if player_bonus.armor_suma <= 0:
        armor = 1
    
    armor = round(player_bonus.armor_suma)
    
    if armor <= 20: # <-- jinak by nefungoval následující generátor čísla 
        bonus_armor = 2
    else:
        bonus_armor = round(armor / 10)
    random_armor = round(random.randint(1, bonus_armor)) # IMPLMENTACE NÁHODNÉHO ARMORU - 10% VARIACE - KVŮLI VĚTŠÍ PESTROSTI SOUBOJŮ
    armor += random_armor

    armor_normal = (armor * pvm_resist) * lvl
    armor_light = (armor * light_resist) * lvl
    armor_heavy = (armor * heavy_resist) * lvl
    armor_magic = (armor * magic_resist) * lvl

    player_hp = player_atributs.suma_hp
    p_deffence = {
        'armor_normal': armor_normal,
        'armor_light': armor_light,
        'armor_heavy': armor_heavy,
        'armor_magic': armor_magic,
        'player_hp': player_hp,
    }

    return p_deffence