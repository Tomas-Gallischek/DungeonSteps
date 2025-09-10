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

# PŘIŘAZENÍ NOVÝCH VLASTNOSTÍ NOVÉHO PŘEDMĚTU
    n = random.randint(1, lvl)
    if n <= 5:
        slots = 0
    elif n <= 15:
        slots = 1
    elif n <= 25:
        slots = 2
    elif n <= 35:
        slots = 3
    else:
        slots = 4

    def bonus_generator():   
        i = random.randint(1, 100)
        if i <= 100:
            luck_koef = 1
        elif i <= 60:
            luck_koef = 2
        elif i <= 30:
            luck_koef = 3
        elif i <= 20:
            luck_koef = 4
        elif i <= 10:
            luck_koef = 5

        random_bonus = random.choice(all_item_bonus)
        random_bonus_id = random_bonus.bonus_id
        bonus_min_value = random_bonus.bonus_min_value
        bonus_max_value = random_bonus.bonus_max_value
        bonus_definitiv_valute = random.randint(bonus_min_value, round(bonus_max_value / 4)) * luck_koef
        if bonus_definitiv_valute > bonus_max_value:
            bonus_definitiv_valute = bonus_max_value

        return bonus_definitiv_valute, random_bonus_id
    
    if slots > 0:
        for one_bonus in range(1, slots + 1):
            bonus_definitiv_valute, random_bonus_id = bonus_generator()

            if random_bonus_id == 1:
                crit_bonus += bonus_definitiv_valute
            else:
                crit_bonus += 0
            if random_bonus_id == 2:
                sance_na_bezvedomi += bonus_definitiv_valute
            else:
                sance_na_bezvedomi += 0
            if random_bonus_id == 3:
                sance_na_otravu += bonus_definitiv_valute
            else:
                sance_na_otravu += 0
            if random_bonus_id == 4:
                poskozeni_utokem += bonus_definitiv_valute
            else:
                poskozeni_utokem += 0
            if random_bonus_id == 5:
                poskozeni_kouzlem += bonus_definitiv_valute
            else:
                poskozeni_kouzlem += 0
            if random_bonus_id == 6:
                pvp_poskozeni += bonus_definitiv_valute
            else:
                pvp_poskozeni += 0
            if random_bonus_id == 7:
                pvm_poskozeni += bonus_definitiv_valute
            else:
                pvm_poskozeni += 0
            if random_bonus_id == 8:
                str_flat_bonus += bonus_definitiv_valute
            else:
                str_flat_bonus += 0
            if random_bonus_id == 9:
                dex_flat_bonus += bonus_definitiv_valute
            else:
                dex_flat_bonus += 0
            if random_bonus_id == 10:
                int_flat_bonus += bonus_definitiv_valute
            else:
                int_flat_bonus += 0
            if random_bonus_id == 11:
                vit_flat_bonus += bonus_definitiv_valute
            else:
                vit_flat_bonus += 0 
            if random_bonus_id == 12:
                luk_flat_bonus += bonus_definitiv_valute
            else:
                luk_flat_bonus += 0
            if random_bonus_id == 13:
                odolnost_proti_bezvedomi += bonus_definitiv_valute
            else:
                odolnost_proti_bezvedomi += 0
            if random_bonus_id == 14:
                odolnost_proti_otrave += bonus_definitiv_valute
            else:
                odolnost_proti_otrave += 0
            if random_bonus_id == 15:
                light_weapon_resist = bonus_definitiv_valute
            else:
                light_weapon_resist = 0
            if random_bonus_id == 16:
                heavy_weapon_resist = bonus_definitiv_valute
            else:
                heavy_weapon_resist = 0
            if random_bonus_id == 17:
                magic_weapon_resist = bonus_definitiv_valute
            else:
                magic_weapon_resist = 0
            if random_bonus_id == 18:
                pvp_resist = bonus_definitiv_valute
            else:
                pvp_resist = 0  
            if random_bonus_id == 19:
                pvm_resist = bonus_definitiv_valute
            else:
                pvm_resist = 0
            if random_bonus_id == 20:
                hp_flat_bonus += bonus_definitiv_valute
            else:
                hp_flat_bonus += 0
# ABY RŮZNÉ KATEGORIE MĚLY RŮZNOU CENU
    if category == 'weapon':
        price_koef = 2
    elif category == 'armor':
        price_koef = 1.5
    else:
        price_koef = 1

    price = 1 * (level_required + level_stop) * (slots + 1) * (lvl / 2) * (random.randint(1, 5)) * price_koef
    price = round(price)


    if category == 'weapon':
        min_dmg_koeficient = random.uniform(1.2, 1.8)
        max_dmg_koeficient = random.uniform(2.5, 3.5)
        min_dmg = round(lvl * 1.5) * min_dmg_koeficient
        max_dmg = round(lvl * 3) * max_dmg_koeficient
        if min_dmg > max_dmg:
            min_dmg, max_dmg = max_dmg, min_dmg
        prum_dmg = (min_dmg + max_dmg) / 2
    else:
        min_dmg = 0
        max_dmg = 0
        prum_dmg = 0

    if category == 'armor':
        armor = round(lvl * 3) + random.randint(0, round(lvl * 2))
    else:
        armor = 0
    if category == 'helmet':
        armor = round(lvl * 2) + random.randint(0, round(lvl * 1.5))   
    else:
        armor = 0 
    if category == 'boots':
        armor = round(lvl * 1.5) + random.randint(0, round(lvl * 1))
    else:
        armor = 0

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
        str_bonus = None
        dex_bonus = None
        int_bonus = None
        vit_bonus = None
        luk_bonus = None

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
        'price': price,
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