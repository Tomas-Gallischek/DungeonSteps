import random
from .models import Mobs
from hracapp.models import Atributs, Playerinfo, Fight, FightLogEntry
import uuid
from .mobs_off_def import mob_attack, mob_deffence
from .player_off_def import player_attack, player_deffence


def pvm_fight_funkce(request):
    WINNER = None
    user = request.user
    atributs = Atributs.objects.get(hrac=user)
    all_mobs = Mobs.objects.all()
    mob = random.choice(all_mobs)
    mob_id = mob.mob_id
    
    # Vytvoření instance Fight namísto proměnné
    fight = Fight.objects.create(
        user=user,
        mob=mob,
    )
    
    print(f"Začíná souboj mezi hráčem {user} a příšerou {mob.name}")


    round_number = 0
    mob_hp = mob.hp
    player_hp = atributs.suma_hp

    player_iniciativa = random.randint(1, 200)
    mob_iniciativa = random.randint(1, 200)

    # Log začátku souboje
    FightLogEntry.objects.create(
        fight=fight,  # Propojení s instancí Fight
        # Odstraněny proměnné 'user' a 'mob'
        round_number=round_number+1,
        description=f"Souboj začíná mezi hráčem {user} a příšerou {mob.name}.",
        event_type="fight_start"
    )

    print("Úspěšné vytvoření logu začátku souboje.")
    while mob_hp > 0 and player_hp > 0:
        round_number += 1
        print(f"round_number č. {round_number}")       

        if player_iniciativa >= mob_iniciativa:
            mob_hp = utok_hrace(request, mob_id, mob_hp, fight, round_number, player_hp)
            if mob_hp <= 0:
                WINNER = str(user)
                print(f"Příšera {mob.name} byla poražena!")
                break
            player_hp = utok_prisery(request, mob_id, player_hp, fight, round_number, mob_hp)
            if player_hp <= 0:
                WINNER = str(mob.name)
                print(f"Hráč {user} byl poražen!")
                break
        if mob_iniciativa > player_iniciativa:
            player_hp = utok_prisery(request, mob_id, player_hp, fight, round_number, mob_hp)
            if player_hp <= 0:
                WINNER = str(mob.name)
                print(f"Hráč {user} byl poražen!")
                break
            mob_hp = utok_hrace(request, mob_id, mob_hp, fight, round_number, player_hp)
            if mob_hp <= 0:
                WINNER = str(user)
                print(f"Příšera {mob.name} byla poražena!")
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


def utok_hrace(request, mob_id, mob_hp, fight, round_number, player_hp):
    print("Hráč útočí")

    p_attack = player_attack(request)
    m_deffence = mob_deffence(request, mob_id)

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

    # Vytvoření záznamu do logu
    FightLogEntry.objects.create(
        fight=fight,
        # Odstraněny proměnné 'user' a 'mob'
        round_number=round_number,
        description=f"Útok hráče: {request.user} Způsobené poškození: {mob_hp_change}, jednalo se o {attack_status} / {attack_type}, životy příšery před útokem: {mob_hp_before}, životy příšery po útoku: {mob_hp_after}",
        player_hp_before=player_hp,
        player_hp_after=player_hp,
        mob_hp_before=mob_hp_before,
        mob_hp_after=mob_hp_after,
        event_type="player_attack"
    )
    return mob_hp


def utok_prisery(request, mob_id, player_hp, fight, round_number, mob_hp):
    print("Příšera útočí")

    mob_name = Mobs.objects.get(mob_id=mob_id)
    m_attack = mob_attack(request, mob_id)
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

    # Vytvoření záznamu do logu
    FightLogEntry.objects.create(
        fight=fight,
        # Odstraněny proměnné 'user' a 'mob'
        round_number=round_number,
        description=f"Útok příšery: {mob_name} Způsobené poškození: {player_hp_change}, jednalo se o {attack_status} / {attack_type}, životy hráče před útokem: {player_hp_before}, životy hráče po útoku: {player_hp_after}",
        player_hp_before=player_hp_before,
        player_hp_after=player_hp_after,
        mob_hp_before=mob_hp,
        mob_hp_after=mob_hp,
        event_type="mob_attack"
    )

    return player_hp