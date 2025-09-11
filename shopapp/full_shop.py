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
        print(f"Vygenerování položky: {new_item['name']}") 

        ShopOffer.objects.create(
            hrac=user,
            item_id=new_item['item_id'],
            name=new_item['name'],
            img_init=new_item['img_init'],
            description=new_item['description'],
            level_required=new_item['level_required'],
            level_stop=new_item['level_stop'],
            item_type=new_item['item_type'],
            item_category=new_item['item_category'],
            slots=new_item['slots'],
            price=new_item['price'],
            sell_price=new_item['sell_price'],
            min_dmg=new_item['min_dmg'],
            max_dmg=new_item['max_dmg'],
            prum_dmg=new_item['prum_dmg'],
            armor=new_item['armor'],

            str_bonus=new_item['str_bonus'],
            dex_bonus=new_item['dex_bonus'],
            int_bonus=new_item['int_bonus'],
            vit_bonus=new_item['vit_bonus'],
            luk_bonus=new_item['luk_bonus'],

            str_flat_it_bonus=new_item['str_flat_bonus'],
            dex_flat_it_bonus=new_item['dex_flat_bonus'],
            int_flat_it_bonus=new_item['int_flat_bonus'],
            vit_flat_it_bonus=new_item['vit_flat_bonus'],
            luck_flat_it_bonus=new_item['luk_flat_bonus'],

            kriticke_poskozeni_procenta_it_bonus=new_item['crit_bonus'],
            sance_na_bezvedomi_procenta_it_bonus=new_item['sance_na_bezvedomi'],
            sance_na_otravu_procenta_it_bonus=new_item['sance_na_otravu'],
            poskozeni_utokem_procenta_it_bonus=new_item['poskozeni_utokem'],
            poskozeni_schopnosti_procenta_it_bonus=new_item['poskozeni_kouzlem'],
            pvp_poskozeni_procenta_it_bonus=new_item['pvp_poskozeni'],
            pvm_poskozeni_procenta_it_bonus=new_item['pvm_poskozeni'],
            bezvedomi_resist_procenta_it_bonus=new_item['odolnost_proti_bezvedomi'],
            otrava_resist_procenta_it_bonus=new_item['odolnost_proti_otrave'],
            light_resist_procenta_it_bonus=new_item['light_weapon_resist'],
            heavy_resist_procenta_it_bonus=new_item['heavy_weapon_resist'],
            magic_resist_procenta_it_bonus=new_item['magic_weapon_resist'],
            pvp_resist_procenta_it_bonus=new_item['pvp_resist'],
            pvm_resist_procenta_it_bonus=new_item['pvm_resist'],
            hp_flat_it_bonus=new_item['hp_flat_bonus']
        )
        print(f"Uložení položky do databáze")

