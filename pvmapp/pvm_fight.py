import random
from .models import Mobs
from hracapp.models import Atributs
from .mobs_off_def import mob_attack, mob_deffence
from .player_off_def import player_attack, player_deffence


# GEMINI MI VYGENEROVAL SUPER NÁVRH NA DATABÁZI LOGŮ, TAK TO UDĚLEJ AŽ NA TO BUDEŠ MÍT SÍLU A ČAS


def pvm_fight_funkce(request):
    WINNER = None
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
        kolo += 1
        print(f"Kolo č. {kolo}")       

        if player_iniciativa >= mob_iniciativa:
            mob_hp = utok_hrace(request, mob_id, mob_hp)
            if mob_hp <= 0:
                WINNER = user
                print(f"Příšera {mob.name} byla poražena!")
                break
            player_hp = utok_prisery(request, mob_id, player_hp)
            if player_hp <= 0:
                WINNER = mob.name
                print(f"Hráč {user} byl poražen!")
                break
        if mob_iniciativa > player_iniciativa:
            player_hp = utok_prisery(request, mob_id, player_hp)
            if player_hp <= 0:
                WINNER = mob.name
                print(f"Hráč {user} byl poražen!")
                break
            mob_hp = utok_hrace(request, mob_id, mob_hp)
            if mob_hp <= 0:
                WINNER = user
                kolo = 0
                print(f"Příšera {mob.name} byla poražena!")
                break




def utok_hrace(request, mob_id, mob_hp):
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

    print(f"Způsobené poškození: {mob_hp_change}, jednalo se o {attack_status} / {attack_type}, životy příšery před útokem: {mob_hp_before}, životy příšery po útoku: {mob_hp_after}")

    return mob_hp


def utok_prisery(request, mob_id, player_hp):
    print("Příšera útočí")

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

    print(f"Způsobené poškození: {player_hp_change}, jednalo se o {attack_status} / {attack_type}, životy hráče před útokem: {player_hp_before}, životy hráče po útoku: {player_hp_after}")
    

    return player_hp








    # NA KONCI ULOŽIT DO FIGHT:LOG CELOU DATABÁZI SOUBOJE (fight log musí být na úrovní hráče)

