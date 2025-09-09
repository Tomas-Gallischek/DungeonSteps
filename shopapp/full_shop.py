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
    for one in range(8):
        print(f"Spuštění generování položek")
        user = request.user
        new_item = items_generator(request)

        
        ShopOffer.objects.create(
            hrac=user,
            item_id=new_item['item_id'],
            item_name=new_item['item_name'],
            img_init=new_item['img_init'],
            description=new_item['description'],
            level_required=new_item['level_required'],
            level_stop=new_item['level_stop'],
            item_type=new_item['item_type'],
            item_category=new_item['item_category'],
            slots=new_item['slots'],
            slot_1_bonus=new_item['slot_1_bonus'],
            slot_1_value=new_item['slot_1_value'],
            slot_2_bonus=new_item['slot_2_bonus'],
            slot_2_value=new_item['slot_2_value'],
            slot_3_bonus=new_item['slot_3_bonus'],
            slot_3_value=new_item['slot_3_value'],
            slot_4_bonus=new_item['slot_4_bonus'],
            slot_4_value=new_item['slot_4_value'],
            price=new_item['price'],
            min_dmg = new_item['min_dmg'],
            max_dmg = new_item['max_dmg'],
            prum_dmg = new_item['prum_dmg'],
            armor=new_item['armor'],
            str_bonus=new_item['str_bonus'],
            dex_bonus=new_item['dex_bonus'],
            int_bonus=new_item['int_bonus'],
            vit_bonus=new_item['vit_bonus'],
            luk_bonus=new_item['luk_bonus'],
        )
        print(f"Uložení položky do databáze")

