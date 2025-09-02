import os
from urllib import request
import django
import sys
import random

GREEN = '\033[92m'
RED = '\033[91m'
RESET = '\033[0m'

def weapons_generator(request):
    from itemsapp.models import Weapons
    user = request.user
    user_name = user.username
    user = user.xp_lvl.first()
    user_lvl = user.lvl
    print(f"{GREEN}Weapon generator SPUŠTĚNÝ{RESET}")
    print(f"{GREEN}Načtení uživatele: {user_name}, Úroveň uživatele: {user_lvl}{RESET}")
    # lvl_required = lvl potřebný na zbraň
    #lvl_stop = lvl, odk kterého se zbraně již nevypisují
    relevant_weapons = []

    weapons = Weapons.objects.all()
    weapons_count = len(weapons)
    for weapon in weapons:
        if weapon.level_required <= user_lvl:
            if weapon.level_stop >= user_lvl:
                relevant_weapons.append(weapon)
            else:
                pass
        else:
            pass
    print(f"{GREEN}Počet relevantních zbraní: {len(relevant_weapons)} z {weapons_count}{RESET}")

    # VÝBĚR KONKRÉTNÍ ZBRANĚ 
    chose_weapon = random.choice(relevant_weapons)
    weapon_name = chose_weapon.name
    weapon_description = chose_weapon.description
    weapon_level_required = chose_weapon.level_required
    weapon_level_stop = chose_weapon.level_stop
    weapon_type = chose_weapon.type
    

    # BASE DMG
    base_dmg = round((((weapon_level_required ** 2) / 2) + (user_lvl)))

    # ZJIŠTĚNÍ ROZPĚTÍ POŠKOZENÍ
    range_lvl_kons = user_lvl
    if range_lvl_kons <= 1:
        range_lvl_kons = 3
    weapon_min_range = round(random.randint(1, round(range_lvl_kons)))
    weapon_max_range = round(random.randint(1, round(range_lvl_kons)))


    # VYPOČÍTÁNÍ POŠKOZENÍ
    weapon_dmg_min = base_dmg - (weapon_min_range)
    if weapon_dmg_min < 1:
        weapon_dmg_min = 1
    weapon_dmg_max = base_dmg + (weapon_max_range)

    rozptyl_zbrane = weapon_dmg_max - weapon_dmg_min

    # ZJIŠTĚNÍ SLOTŮ PRO ATRIBUTY
    slots_number = random.randint(1, user_lvl)

    if slots_number >= 5:
        pocet_slotu = 1
        if slots_number >= 10:
            pocet_slotu = 2
            if slots_number >= 20:
                pocet_slotu = 3
                if slots_number >= 30:
                    pocet_slotu = 4
    else:
        pocet_slotu = 0

    weapon_price = int(random.randint(1, weapon_level_required)*user_lvl)
    # DODĚLAT BONUSY ZBRANĚ

    result = {
        'weapon_name': weapon_name,
        'weapon_description': weapon_description,
        'weapon_level_required': weapon_level_required,
        'weapon_level_stop': weapon_level_stop,
        'weapon_type': weapon_type,
        'weapon_base_damage': base_dmg,
        'weapon_min_damage': weapon_dmg_min,
        'weapon_max_damage': weapon_dmg_max,
        'weapon_slots': pocet_slotu,
        'weapon_price': weapon_price,
        # DOPSAT ATRIBUTY AŽ BUDOU

    }

    print(f"{GREEN}Vybraná zbraň: {chose_weapon.name}{RESET}")
    print(f"{GREEN}Statistiky zbraně:{RESET}")
    print(f"  Požadovaná úroveň: {chose_weapon.level_required}")
    print(f"  Základní poškození: {base_dmg}")
    print(f"  Rozsah poškození: {weapon_dmg_min} - {weapon_dmg_max} ({rozptyl_zbrane})")
    print(f"  Počet slotů pro atributy: {pocet_slotu}")
    print(f"  Cena zbraně: {weapon_price} zlaťáků")

    print(f"{GREEN}Zbraně pro {user_name} byly vygenerovány.{RESET}")
    result = {
        "status": "success",
    }
    return result, weapon_name, weapon_description, weapon_level_required, weapon_level_stop, weapon_type, base_dmg, weapon_dmg_min, weapon_dmg_max, pocet_slotu, weapon_price



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
    from itemsapp.models import Weapons
    # Spuštění testu s konkrétním uživatelem
    user = Playerinfo.objects.get(username='Shrek')
    result = weapons_generator(user)