from pickle import NONE
import random
from .models import Mobs
from django.contrib.auth.decorators import login_required


@login_required
def mob_info(mob_id):
    mob = Mobs.objects.get(mob_id=mob_id)
    name = mob.name
    lvl = mob.lvl

    hp = mob.hp
    str = mob.str
    dex = mob.dex
    int = mob.int
    vit = mob.vit
    luck = mob.luck
    armor = mob.armor

    m_info = {
        'name': name,
        'lvl': lvl,
        'hp': hp,
        'str': str,
        'dex': dex,
        'int': int,
        'vit': vit,
        'luck': luck,
        'armor': armor,
    }

    return m_info

@login_required
def mob_attack(request, mob_id):
    mob = Mobs.objects.get(mob_id=mob_id)
    str = mob.str
    dex = mob.dex
    int = mob.int

    dmg_atr = mob.dmg_atr

    if dmg_atr == 'strength':
        dmg_atr_value = str / 10
        attack_type = 'heavy' 
    elif dmg_atr == 'dexterity':
        dmg_atr_value = dex / 10
        attack_type = 'light'
    elif dmg_atr == 'intelligence':
        dmg_atr_value = int / 10
        attack_type = 'magic'
    else:
        dmg_atr_value = 1
        attack_type = None

    poskozeni_schopnosti = mob.poskozeni_schopnosti
    poskozeni_utokem = mob.poskozeni_utokem
    sance_na_otravu = mob.sance_na_otravu
    sance_na_bezvedomi = mob.sance_na_bezvedomi
    sance_na_kriticky_utok = mob.sance_na_kriticky_utok
    kriticke_poskozeni = mob.kriticke_poskozeni



    min_dmg = round(mob.min_dmg)
    max_dmg = round(mob.max_dmg)

    random_dmg = random.randint(min_dmg, max_dmg)

    final_attack = round(random_dmg * dmg_atr_value) * poskozeni_utokem
    attack_status = "normální zásah"


    if random.randint(1, 100) <= sance_na_kriticky_utok:
        final_attack = round(final_attack * (2 + kriticke_poskozeni))
        attack_status = "kritický zásah"

    m_attack = {
        'final_attack': final_attack,
        'attack_status': attack_status,
        'attack_type': attack_type,
    }

    return m_attack


@login_required
def mob_deffence(request, mob_id):
    mob = Mobs.objects.get(mob_id=mob_id)

    hp = mob.hp

    heavy_resist = mob.heavy_resist + (mob.str / 1000)
    magic_resist = mob.magic_resist + (mob.int / 1000)
    light_resist = mob.light_resist + (mob.dex / 1000)
    # light_resist_procenta_it_bonus =
    # otrava_resist_procenta_it_bonus = 
    # bezvedomi_resist_procenta_it_bonus = 

    armor = mob.armor
    bonus_armor = round(armor / 10)
    random_armor = round(random.randint(1, bonus_armor)) # IMPLMENTACE NÁHODNÉHO ARMORU - 10% VARIACE - KVŮLI VĚTŠÍ PESTROSTI SOUBOJŮ
    armor += random_armor

    armor_light = (armor * light_resist)
    armor_heavy = (armor * heavy_resist)
    armor_magic = (armor * magic_resist)


    m_deffence = {
        'armor_normal': armor,
        'armor_light': armor_light,
        'armor_heavy': armor_heavy,
        'armor_magic': armor_magic,
        'mob_hp': hp,
    }

    return m_deffence