from hmac import new
import random
import re
from itemsapp import weapons
from hracapp.models import Playerinfo

def full_shop(request):
    print(f"Spuštění funkce naplnění obchodu")
    # Smazání všech existujících nabídek
    request.user.shop_offers.all().delete()
    typy_itemu = ['weapon']
    item_id = 1
    for one in range(6):
        print(f"Spuštění generování položek")
# ZÁKLADNÍ NASTAVENÍ A INPORTY
        user = request.user
        new_item = user.shop_offers.create()
        result, weapon_name, weapon_description, weapon_level_required, weapon_level_stop, weapon_type, base_dmg, weapon_dmg_min, weapon_dmg_max, pocet_slotu, weapon_price = weapons.weapons_generator(request)
# GENEROVÁNÍ UNIKÁTNÍHO ID
        item_id_generace = [str(weapon_level_required), str(weapon_level_stop), str(base_dmg), str(weapon_dmg_min), str(weapon_dmg_max), str(pocet_slotu), str(weapon_price), str(random.randint(1, 99))]
        id_conver_number = "".join(item_id_generace)
        item_id = int(id_conver_number)
# uložení vygenerovaného itemu do databáze
        new_item.item_id = item_id
        item_type = random.choice(typy_itemu)[0]
        new_item.item_type = item_type
        print(f"Nastavení typu položky: {item_type}")
        new_item.item_name = weapon_name
        print(f"Nastavení názvu položky: {weapon_name}")
        new_item.item_price = weapon_price
        print(f"Nastavení ceny položky: {weapon_price}")
        new_item.item_description = weapon_description
        print(f"Nastavení popisu položky: {weapon_description}")
        new_item.item_level_required = weapon_level_required
        print(f"Nastavení požadované úrovně položky: {weapon_level_required}")
        new_item.item_level_stop = weapon_level_stop
        print(f"Nastavení zastavení úrovně položky: {weapon_level_stop}")
        new_item.item_weapon_type = weapon_type
        print(f"Nastavení typu zbraně položky: {weapon_type}")
        new_item.item_base_damage = base_dmg
        new_item.item_min_damage = weapon_dmg_min
        new_item.item_max_damage = weapon_dmg_max
        new_item.item_slots = pocet_slotu
        print(f"Nastavení parametrů zbraně: {base_dmg}, {weapon_dmg_min}, {weapon_dmg_max}, {pocet_slotu}")
        

        new_item.save()
        print(f"Uložení položky do databáze")

