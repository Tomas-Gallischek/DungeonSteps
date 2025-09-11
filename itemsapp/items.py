from calendar import c
import os
from turtle import st
from urllib import request
import django
import sys
import random
from hracapp.models import XP_LVL


GREEN = '\033[92m'
RED = '\033[91m'
RESET = '\033[0m'

def items_generator(request):
    from .models import Items_bonus, Items

    user = request.user
    lvl = XP_LVL.objects.get(hrac=user).lvl
    rasa = user.rasa
    povolani = user.povolani
    item_type = user.item_type

    print(f"Generuji předmět pro uživatele: {user}, level: {lvl}, rasa: {rasa}, povolani: {povolani}")

# FILTRACE VŠECH EXISTUJÍCÍCH PŘEDMĚTŮ VE HŘE
    all_items = Items.objects.all()
    all_item_bonus = Items_bonus.objects.all()
# FILTRACE PODLE LEVELU
    relevant_items = [item for item in all_items if item.level_required <= lvl <= item.level_stop]  
# FILTRACE PODLE POVOLÁNÍ
    relevant_items = [item for item in relevant_items if item.item_type == item_type or item.item_type == 'universal']

# VÝBĚR NÁHODNÉHO PŘEDMĚTU
    new_item = random.choice(relevant_items)

# PŘIŘAZENÍ -- již existujících -- VLASTNOSTÍ NOVÉHO PŘEDMĚTU
    name = new_item.name
    id_random = random.randint(1, 999999)
    item_id = id_random
    img_init = new_item.img_init
    description = new_item.description
    level_required = new_item.level_required
    level_stop = new_item.level_stop
    type = new_item.item_type
    category = new_item.item_category

    print(f"Kategorie vybraného itemu: {category}")

# PŘIŘAZENÍ NOVÝCH VLASTNOSTÍ NOVÉHO PŘEDMĚTU
    n = random.randint(1, lvl)
    if n <= 5:
        slots = 0
    elif n <= 10:
        slots = 1
    elif n <= 20:
        slots = 2
    elif n <= 30:
        slots = 3
    else:
        slots = 4

    numbers = random.sample(range(1, 20 + 1), slots)

    crit_bonus = 0
    if 1 in numbers:
        min_value = all_item_bonus.get(bonus_id = 1).bonus_min_value
        max_value = all_item_bonus.get(bonus_id = 1).bonus_max_value
        crit_bonus = random.randint((min_value * 10), (max_value * 10))
        crit_bonus = crit_bonus / 10
    
    sance_na_bezvedomi = 0
    if 2 in numbers:
        min_value = all_item_bonus.get(bonus_id = 2).bonus_min_value
        max_value = all_item_bonus.get(bonus_id = 2).bonus_max_value
        sance_na_bezvedomi = random.randint((min_value * 10), (max_value * 10))
        sance_na_bezvedomi = sance_na_bezvedomi / 10

    sance_na_otravu = 0
    if 3 in numbers:
        min_value = all_item_bonus.get(bonus_id = 3).bonus_min_value
        max_value = all_item_bonus.get(bonus_id = 3).bonus_max_value
        sance_na_otravu = random.randint((min_value * 10), (max_value * 10))
        sance_na_otravu = sance_na_otravu / 10

    poskozeni_utokem = 0
    if 4 in numbers:
        min_value = all_item_bonus.get(bonus_id = 4).bonus_min_value
        max_value = all_item_bonus.get(bonus_id = 4).bonus_max_value
        poskozeni_utokem = random.randint((min_value * 10), (max_value * 10))
        poskozeni_utokem = poskozeni_utokem / 10

    poskozeni_kouzlem = 0
    if 5 in numbers:
        min_value = all_item_bonus.get(bonus_id = 5).bonus_min_value
        max_value = all_item_bonus.get(bonus_id = 5).bonus_max_value
        poskozeni_kouzlem = random.randint((min_value * 10), (max_value * 10))
        poskozeni_kouzlem = poskozeni_kouzlem / 10


    pvp_poskozeni = 0
    if 6 in numbers:
        min_value = all_item_bonus.get(bonus_id = 6).bonus_min_value
        max_value = all_item_bonus.get(bonus_id = 6).bonus_max_value
        pvp_poskozeni = random.randint((min_value * 10), (max_value * 10))
        pvp_poskozeni = pvp_poskozeni / 10


    pvm_poskozeni = 0
    if 7 in numbers:
        min_value = all_item_bonus.get(bonus_id = 7).bonus_min_value
        max_value = all_item_bonus.get(bonus_id = 7).bonus_max_value
        pvm_poskozeni = random.randint((min_value * 10), (max_value * 10))
        pvm_poskozeni = pvm_poskozeni / 10

    str_flat_bonus = 0
    if 8 in numbers:
        min_value = all_item_bonus.get(bonus_id = 8).bonus_min_value
        max_value = all_item_bonus.get(bonus_id = 8).bonus_max_value
        str_flat_bonus = random.randint(min_value, max_value)


    dex_flat_bonus = 0
    if 9 in numbers:
        min_value = all_item_bonus.get(bonus_id = 9).bonus_min_value
        max_value = all_item_bonus.get(bonus_id = 9).bonus_max_value
        dex_flat_bonus = random.randint(min_value, max_value)


    int_flat_bonus = 0
    if 10 in numbers:   
        min_value = all_item_bonus.get(bonus_id = 10).bonus_min_value
        max_value = all_item_bonus.get(bonus_id = 10).bonus_max_value
        int_flat_bonus = random.randint(min_value, max_value)


    vit_flat_bonus = 0
    if 11 in numbers:
        min_value = all_item_bonus.get(bonus_id = 11).bonus_min_value
        max_value = all_item_bonus.get(bonus_id = 11).bonus_max_value
        vit_flat_bonus = random.randint(min_value, max_value)
    
    luk_flat_bonus = 0
    if 12 in numbers:
        min_value = all_item_bonus.get(bonus_id = 12).bonus_min_value
        max_value = all_item_bonus.get(bonus_id = 12).bonus_max_value
        luk_flat_bonus = random.randint(min_value, max_value)

    odolnost_proti_bezvedomi = 0
    if 13 in numbers:
        min_value = all_item_bonus.get(bonus_id = 13).bonus_min_value
        max_value = all_item_bonus.get(bonus_id = 13).bonus_max_value
        odolnost_proti_bezvedomi = random.randint((min_value * 10), (max_value * 10))
        odolnost_proti_bezvedomi = odolnost_proti_bezvedomi / 10

    odolnost_proti_otrave = 0
    if 14 in numbers:
        min_value = all_item_bonus.get(bonus_id = 14).bonus_min_value
        max_value = all_item_bonus.get(bonus_id = 14).bonus_max_value
        odolnost_proti_otrave = random.randint((min_value * 10), (max_value * 10))
        odolnost_proti_otrave = odolnost_proti_otrave / 10

    light_weapon_resist = 0
    if 15 in numbers:
        min_value = all_item_bonus.get(bonus_id = 15).bonus_min_value
        max_value = all_item_bonus.get(bonus_id = 15).bonus_max_value
        light_weapon_resist = random.randint((min_value * 10), (max_value * 10))
        light_weapon_resist = light_weapon_resist / 10
    
    heavy_weapon_resist = 0
    if 16 in numbers:
        min_value = all_item_bonus.get(bonus_id = 16).bonus_min_value
        max_value = all_item_bonus.get(bonus_id = 16).bonus_max_value
        heavy_weapon_resist = random.randint((min_value * 10), (max_value * 10))
        heavy_weapon_resist = heavy_weapon_resist / 10

    magic_weapon_resist = 0
    if 17 in numbers:
        min_value = all_item_bonus.get(bonus_id = 17).bonus_min_value
        max_value = all_item_bonus.get(bonus_id = 17).bonus_max_value
        magic_weapon_resist = random.randint((min_value * 10), (max_value * 10))
        magic_weapon_resist = magic_weapon_resist / 10

    
    pvp_resist = 0
    if 18 in numbers:
        min_value = all_item_bonus.get(bonus_id = 18).bonus_min_value
        max_value = all_item_bonus.get(bonus_id = 18).bonus_max_value
        pvp_resist = random.randint((min_value * 10), (max_value * 10))
        pvp_resist = pvp_resist / 10

    pvm_resist = 0
    if 19 in numbers:
        min_value = all_item_bonus.get(bonus_id = 19).bonus_min_value
        max_value = all_item_bonus.get(bonus_id = 19).bonus_max_value
        pvm_resist = random.randint((min_value * 10), (max_value * 10))
        pvm_resist = pvm_resist / 10

    hp_flat_bonus = 0
    if 20 in numbers:
        min_value = all_item_bonus.get(bonus_id = 20).bonus_min_value
        max_value = all_item_bonus.get(bonus_id = 20).bonus_max_value
        hp_flat_bonus = random.randint(min_value, max_value)

    print(f"Náhodné čísla: {numbers} - Počet slotů: {slots}")


# ABY RŮZNÉ KATEGORIE MĚLY RŮZNOU CENU
    if category == 'weapon':
        price_koef = 2
    elif category == 'armor':
        price_koef = 1.5
    else:
        price_koef = 1

    price = 1 * (level_required + level_stop) * (slots + 1) * (lvl / 2) * (random.randint(1, 5)) * price_koef
    price = round(price)
    sell_price = round(price / 2)


    if category == 'weapon':
        min_dmg_koeficient = random.uniform(1.2, 1.8)
        max_dmg_koeficient = random.uniform(2.5, 3.5)
        min_dmg = round(lvl * 1.5) * min_dmg_koeficient
        max_dmg = round(lvl * 3) * max_dmg_koeficient
        if min_dmg > max_dmg:
            min_dmg, max_dmg = max_dmg, min_dmg
        prum_dmg = round((min_dmg + max_dmg) / 2)

# JELIKOŽ PROTI UNIVERZÁLNÍM ZBRANÍM NEEXISTUJÍ ZATÍM RESISTENCE, JE TŘEBA JE UŽ V ZÁKLADU OSLABIT
        if item_type == 'universal':
            min_dmg = round(min_dmg * 0.8)
            max_dmg = round(max_dmg * 0.8)
            prum_dmg = round(prum_dmg * 0.8)
    else:
        min_dmg = 0
        max_dmg = 0
        prum_dmg = 0


    if category == 'armor':
        armor = round(lvl * 3) + random.randint(0, round(lvl * 2))

    elif category == 'helmet':
        armor = round(lvl * 2) + random.randint(0, round(lvl * 1.5))   

    elif category == 'boots':
        armor = round(lvl * 1.5) + random.randint(0, round(lvl * 1))
    else:
        armor = 0

    print(GREEN + f"ARMOR: {armor}, Kategorie itemu: {category}" + RESET)

    if category in ['ring', 'amulet', 'talisman']:
        str_bonus = random.randint(0, round(lvl * 1.5))
        if str_bonus < lvl:
            str_bonus = 0
        dex_bonus = random.randint(0, round(lvl * 1.5))
        if dex_bonus < lvl:
            dex_bonus = 0
        int_bonus = random.randint(0, round(lvl * 1.5))
        if int_bonus < lvl:
            int_bonus = 0
        vit_bonus = random.randint(0, round(lvl * 1.5))
        if vit_bonus < lvl:
            vit_bonus = 0
        luk_bonus = random.randint(0, round(lvl * 1.5))
        if luk_bonus < lvl:
            luk_bonus = 0

        if str_bonus == 0 and dex_bonus == 0 and int_bonus == 0 and vit_bonus == 0 and luk_bonus == 0:
            i = random.randint(1, 5)
            if i == 1:
                str_bonus = random.randint(lvl, round(lvl * 1.5))
            elif i == 2:
                dex_bonus = random.randint(lvl, round(lvl * 1.5))
            elif i == 3:
                int_bonus = random.randint(lvl, round(lvl * 1.5))
            elif i == 4:
                vit_bonus = random.randint(lvl, round(lvl * 1.5))
            elif i == 5:
                luk_bonus = random.randint(lvl, round(lvl * 1.5))

    else:
        str_bonus = 0
        dex_bonus = 0
        int_bonus = 0
        vit_bonus = 0
        luk_bonus = 0

    new_item = {
        'name': name,
        'item_id': item_id,
        'img_init': img_init,
        'description': description,
        'level_required': level_required,
        'level_stop': level_stop,
        'item_type': type,
        'item_category': category,
        'slots': slots,

        'crit_bonus': crit_bonus,
        'sance_na_bezvedomi': sance_na_bezvedomi,
        'sance_na_otravu': sance_na_otravu,
        'poskozeni_utokem': poskozeni_utokem,
        'poskozeni_kouzlem': poskozeni_kouzlem,
        'pvp_poskozeni': pvp_poskozeni,
        'pvm_poskozeni': pvm_poskozeni,

        'str_flat_bonus': str_flat_bonus,
        'dex_flat_bonus': dex_flat_bonus,
        'int_flat_bonus': int_flat_bonus,
        'vit_flat_bonus': vit_flat_bonus,
        'luk_flat_bonus': luk_flat_bonus,

        'odolnost_proti_bezvedomi': odolnost_proti_bezvedomi,
        'odolnost_proti_otrave': odolnost_proti_otrave,
        'light_weapon_resist': light_weapon_resist,
        'heavy_weapon_resist': heavy_weapon_resist,
        'magic_weapon_resist': magic_weapon_resist,
        'pvp_resist': pvp_resist,
        'pvm_resist': pvm_resist,
        'hp_flat_bonus': hp_flat_bonus,

        'price': price,
        'sell_price': sell_price,
        'min_dmg': min_dmg,
        'max_dmg': max_dmg,
        'prum_dmg': prum_dmg,
        'armor': armor,
        
        'str_bonus': str_bonus,
        'dex_bonus': dex_bonus,
        'int_bonus': int_bonus,
        'vit_bonus': vit_bonus,
        'luk_bonus': luk_bonus,
    }

    return new_item



#   PRO SPUŠTĚNÍ SKRIPTU 
if __name__ == "__main__": # <-- KÓD PRO SPRÁVNÉ SPUŠTĚNÍ PŘI TESTOVÁNÍ FUNKCE + IMPORT DATABÁZE
    # Nastavení Django prostředí
    # Zde se ujistíte, že je správná cesta k projektu na Python path
    current_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(current_dir)
    sys.path.append(project_root)

    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'houska.settings')
    django.setup()
    
    # Import modelu se nyní provádí až po nastavení Django prostředí
    from hracapp.models import Playerinfo
    from itemsapp.models import Items
    # Spuštění testu s konkrétním uživatelem
    request = {


    }

    print(f"Testuji generátor předmětů pro uživatele: {request['user']}")
    result = items_generator(request)