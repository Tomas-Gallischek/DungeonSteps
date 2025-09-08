from hmac import new
import random
from re import I
from itemsapp.items import items_generator
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
        new_item = items_generator(request)
        
# GENEROVÁNÍ UNIKÁTNÍHO ID
        item_id_generace = [str(new_item['level_required']), str(new_item['level_stop']), str(new_item['base_damage']), str(new_item['min_damage']), str(new_item['max_damage']), str(new_item['slots']), str(new_item['price']), str(random.randint(1, 99))]
        id_conver_number = "".join(item_id_generace)
        item_id = int(id_conver_number)
        item_type = random.choice(typy_itemu)[0]

        ShopOffer.objects.create(
            hrac=user,
            item_id=item_id,
            item_type=item_type,
            item_data=new_item
        )
        print(f"Uložení položky do databáze")

