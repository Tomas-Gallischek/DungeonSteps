import random
from .models import Mobs
from hracapp.models import Atributs
from .mobs_off_def import mob_attack, mob_deffence
from .player_off_def import player_attack, player_deffence


def pvm_fight_funkce(request):
    user = request.user
    atributs = Atributs.objects.get(hrac=user)
    all_mobs = Mobs.objects.all()
    mob = random.choice(all_mobs)
    mob_id = mob.mob_id
    print(f"Začíná souboj mezi hráčem {user} a příšerou {mob.name}")

    kolo = 1
    mob_hp = mob.hp
    player_hp = atributs.suma_hp

    player_iniciativa = random.randint(1, 200)
    mob_iniciativa = random.randint(1, 200)

    while mob_hp > 0 and player_hp > 0:
        print(f"Kolo č. {kolo}")       

        if player_iniciativa >= mob_iniciativa:
            mob_hp = utok_hrace(request, user, mob_id, mob_hp, mob)
            if mob_hp <= 0:
                WINNER = user
                print(f"Příšera {mob.name} byla poražena!")
                break
            player_hp = utok_prisery(request, user, mob_id, player_hp, mob)
            if player_hp <= 0:
                WINNER = mob.name
                print(f"Hráč {user} byl poražen!")
                break
        if mob_iniciativa > player_iniciativa:
            player_hp = utok_prisery(request, user, mob_id, player_hp, mob)
            if player_hp <= 0:
                WINNER = mob.name
                print(f"Hráč {user} byl poražen!")
                break
            mob_hp = utok_hrace(request, user, mob_id, mob_hp, mob)
            if mob_hp <= 0:
                WINNER = user
                print(f"Příšera {mob.name} byla poražena!")
                break




def utok_hrace(request, user, mob_id, mob_hp, mob):
    print("Hráč útočí")

    p_attack = player_attack(request)
    m_deffence = mob_deffence(mob_id)

    attack_status = p_attack['attack_status']

    if p_attack['attack_type'] == 'light':
        dmg = p_attack['final_attack'] - m_deffence['armor_light']
    elif p_attack['attack_type'] == 'heavy':
        dmg = p_attack['final_attack'] - m_deffence['armor_heavy']
    elif p_attack['attack_type'] == 'magic':
        dmg = p_attack['final_attack'] - m_deffence['armor_magic']
    else:
        dmg = p_attack['final_attack'] - m_deffence['armor']

    if dmg < 0:
        dmg = 0

    mob_hp_before = mob_hp
    mob_hp_change = round(dmg)
    mob_hp_after = mob_hp_before - mob_hp_change
    mob_hp = mob_hp_after

    return mob_hp


def utok_prisery(request, user, mob_id, player_hp, mob):
    print("Příšera útočí")

    m_attack = mob_attack(mob_id)
    p_deffence = player_deffence(request)

    attack_status = m_attack['attack_status']

    if m_attack['attack_type'] == 'light':
        dmg = m_attack['final_attack'] - p_deffence['armor_light']
    elif m_attack['attack_type'] == 'heavy':
        dmg = m_attack['final_attack'] - p_deffence['armor_heavy']
    elif m_attack['attack_type'] == 'magic':
        dmg = m_attack['final_attack'] - p_deffence['armor_magic']
    else:
        dmg = m_attack['final_attack'] - p_deffence['armor']

    if dmg < 0:
        dmg = 0

    player_hp_before = player_hp
    player_hp_change = round(dmg)
    player_hp_after = player_hp_before - player_hp_change
    player_hp = player_hp_after

    return player_hp








    # NA KONCI ULOŽIT DO FIGHT:LOG CELOU DATABÁZI SOUBOJE (fight log musí být na úrovní hráče)

