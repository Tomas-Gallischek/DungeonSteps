from hmac import new
import random
from itemsapp import weapons
from hracapp.models import Playerinfo, ShopOffer

def full_shop(request):
    print(f"Spuštění funkce naplnění obchodu")
    # Smazání všech existujících nabídek
    ShopOffer.objects.all().delete()
    user = request.user
    shop_offers = ShopOffer.objects.filter(hrac=user)
    shop_offers.delete()
    typy_itemu = ['weapon']
    item_id = 1
    for one in range(6):
        print(f"Spuštění generování položek")
# ZÁKLADNÍ NASTAVENÍ A INPORTY
        user = request.user
        result, weapon_name, weapon_description, weapon_level_required, weapon_level_stop, weapon_type, base_dmg, weapon_dmg_min, weapon_dmg_max, pocet_slotu, weapon_price = weapons.weapons_generator(request)
        
# GENEROVÁNÍ UNIKÁTNÍHO ID
        item_id_generace = [str(weapon_level_required), str(weapon_level_stop), str(base_dmg), str(weapon_dmg_min), str(weapon_dmg_max), str(pocet_slotu), str(weapon_price), str(random.randint(1, 99))]
        id_conver_number = "".join(item_id_generace)
        item_id = int(id_conver_number)
        item_type = random.choice(typy_itemu)[0]

        ShopOffer.objects.create(
            hrac=user,
            item_id=item_id,
            item_type=item_type,
            item_name=weapon_name,
            item_price=weapon_price,
            item_description=weapon_description,
            item_level_required=weapon_level_required,
            item_level_stop=weapon_level_stop,
            item_weapon_type=weapon_type,
            item_base_damage=base_dmg,
            item_min_damage=weapon_dmg_min,
            item_max_damage=weapon_dmg_max,
            item_slots=pocet_slotu
        )
        print(f"Uložení položky do databáze")

