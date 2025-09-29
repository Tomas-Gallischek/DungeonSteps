from email.mime import base
from multiprocessing import Value
import random
import re
from .models import Mobs_random
from hracapp.models import Atributs, Playerinfo, Fight, FightLogEntry
import uuid
from .mobs_off_def import mob_attack, mob_deffence
from .player_off_def import player_attack, player_deffence


def pvm_fight_funkce(request, mob):
    WINNER = None
    user = request.user
    atributs = Atributs.objects.get(hrac=user)
    mob_id = mob['mob_id']
    remaining_hp_percent = 100
    
    # Vytvoření instance Fight namísto proměnné
    fight = Fight.objects.create(
        user=user,
        mob=mob['name'],
    )
    
    print(f"Začíná souboj mezi hráčem {user} a příšerou {mob['name']} (ID: {mob_id})")


    round_number = 0
    mob_hp = mob['hp']
    mob_default_hp = mob_hp
    player_hp = atributs.suma_hp
    player_default_hp = player_hp

    player_iniciativa = random.randint(1, 200)
    mob_iniciativa = random.randint(1, 200)

    # Log začátku souboje
    FightLogEntry.objects.create(
        fight=fight,
        round_number=round_number+1,
        description=f"Souboj začíná mezi hráčem {user} a příšerou {mob['name']}.",
        event_type="fight_start"
    )
    print("Úspěšné vytvoření logu začátku souboje.")
    
    while mob_hp > 0 and player_hp > 0:
        round_number += 1     

        if player_iniciativa >= mob_iniciativa:
            mob_hp = utok_hrace(request, mob, mob_hp, fight, round_number, player_hp, mob_default_hp, player_default_hp, remaining_hp_percent)
            if mob_hp <= 0:
                WINNER = str(user)
                print(f"Příšera {mob['name']} byla poražena!")
                break
            player_hp = utok_prisery(request, mob, player_hp, fight, round_number, mob_hp, mob_default_hp, player_default_hp, remaining_hp_percent)
            if player_hp <= 0:
                WINNER = str(mob['name'])
                print(f"Hráč {user} byl poražen!")
                break
        if mob_iniciativa > player_iniciativa:
            player_hp = utok_prisery(request, mob, player_hp, fight, round_number, mob_hp, mob_default_hp, player_default_hp, remaining_hp_percent)
            if player_hp <= 0:
                WINNER = str(mob['name'])
                print(f"Hráč {user} byl poražen!")
                break
            mob_hp = utok_hrace(request, mob, mob_hp, fight, round_number, player_hp, mob_default_hp, player_default_hp, remaining_hp_percent)
            if mob_hp <= 0:
                WINNER = str(user)
                print(f"Příšera {mob['name']} byla poražena!")
                break
    if WINNER:
        winner_name = WINNER
        fight.winner = winner_name
        fight.save() # Uložíme vítěze v instanci Fight
        
        FightLogEntry.objects.create(
            fight=fight,
            # Odstraněny proměnné 'user' a 'mob'
            round_number=round_number,
            description=f"Souboj končí. Vítězem je {winner_name}.",
            event_type="fight_end",
            player_hp_after=player_hp,
            player_hp_before=player_hp,
            mob_hp_before=mob_hp,
            mob_hp_after=mob_hp,
        )
    return fight.fight_id


def utok_hrace(request, mob, mob_hp, fight, round_number, player_hp, mob_default_hp, player_default_hp, remaining_hp_percent):
    p_attack = player_attack(request)
    m_deffence = mob_deffence(request, mob)

    attack_status = p_attack['attack_status']
    attack_type = p_attack['attack_type']

    if attack_type == 'light':
        dmg = p_attack['final_attack'] - m_deffence['armor_light']
    elif attack_type == 'heavy':
        dmg = p_attack['final_attack'] - m_deffence['armor_heavy']
    elif attack_type == 'magic':
        dmg = p_attack['final_attack'] - m_deffence['armor_magic']
    else:
        dmg = p_attack['final_attack'] - m_deffence['armor_normal']

    if dmg < 0:
        dmg = 0

    mob_hp_before = mob_hp
    mob_hp_change = round(dmg)
    mob_hp_after = mob_hp_before - mob_hp_change
    mob_hp = mob_hp_after
    minus_hp_percent = round((mob_hp_change / mob_default_hp) * 100)


    remaining_hp_percent = round((mob_hp_after / mob_default_hp) * 100)


    FightLogEntry.objects.create(
        fight=fight,
        round_number=round_number,
        event_type="player_attack",
        attack_type=attack_type,
        attack_status=attack_status,
        player_hp_before=player_hp,
        player_hp_after=player_hp,
        mob_hp_before=mob_hp_before,
        mob_hp_after=mob_hp_after,
        dmg=dmg,
        attack_value = p_attack['final_attack'],
        defence_value = p_attack['final_attack'] - dmg, # protože záleží, čím se obránce brání
        base_armor = mob['armor'],
        minus_hp_percent = minus_hp_percent,
        description=f"Útok hráče: {request.user} Způsobené poškození: {mob_hp_change}, jednalo se o {attack_status} / {attack_type}, životy příšery před útokem: {mob_hp_before}, životy příšery po útoku: {mob_hp_after}, Základní obrana: {mob['armor']}, HP = -{minus_hp_percent}% ({remaining_hp_percent}% zbývá)"
    )   
    return mob_hp


def utok_prisery(request, mob, player_hp, fight, round_number, mob_hp, mob_default_hp, player_default_hp, remaining_hp_percent):

    m_attack = mob_attack(request, mob)
    p_deffence = player_deffence(request)

    attack_status = m_attack['attack_status']
    attack_type = m_attack['attack_type']

    if attack_type == 'light':
        dmg = m_attack['final_attack'] - p_deffence['armor_light']
    elif attack_type == 'heavy':
        dmg = m_attack['final_attack'] - p_deffence['armor_heavy']
    elif attack_type == 'magic':
        dmg = m_attack['final_attack'] - p_deffence['armor_magic']
    else:
        dmg = m_attack['final_attack'] - p_deffence['armor_normal']

    if dmg < 0:
        dmg = 0

    player_hp_before = player_hp
    player_hp_change = round(dmg)
    player_hp_after = player_hp_before - player_hp_change
    player_hp = player_hp_after
    minus_hp_percent = round((player_hp_change / player_default_hp) * 100)

    remaining_hp_percent = round((player_hp_after / player_default_hp) * 100)

    # Vytvoření záznamu do logu
    FightLogEntry.objects.create(
        fight=fight,
        round_number=round_number,
        event_type="mob_attack",
        attack_type=attack_type,
        attack_status=attack_status,
        player_hp_before=player_hp_before,
        player_hp_after=player_hp_after,
        mob_hp_before=mob_hp,
        mob_hp_after=mob_hp,
        dmg=dmg,
        attack_value = m_attack['final_attack'],
        defence_value = m_attack['final_attack'] - dmg, # protože záleží, čím se obránce brání
        base_armor = p_deffence['armor_normal'],
        minus_hp_percent = minus_hp_percent,
        description=f"Útok příšery: {mob['name']} Způsobené poškození: {player_hp_change}, jednalo se o {attack_status} / {attack_type}, životy hráče před útokem: {player_hp_before}, životy hráče po útoku: {player_hp_after}, Obrana: {p_deffence['armor_normal']} HP = -{minus_hp_percent}% ({remaining_hp_percent}% zbývá)"
    )

    return player_hp