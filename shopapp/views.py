from multiprocessing import context
from django.urls import reverse
from .full_shop import full_shop
from django.shortcuts import redirect, render
from hracapp.models import ShopOffer, INV, Economy
from django.contrib.auth.decorators import login_required
from hracapp.economy import buy_or_sell

@login_required
def shop(request):
    print(f"Spuštění funkce renderování obchodu")
    user = request.user
    items = ShopOffer.objects.all()
    items_in_shop = items
    context = {
        'user': user,
        'items_in_shop': items_in_shop,
    }

    return render(request, 'shopapp/shop.html', context)


def shop_reset(request):
    print(f"Spuštění funkce resetování obchodu")
    user = request.user
    vypis = full_shop(request)
    items_in_shop = ShopOffer.objects.all()
    context = {
        'user': user,
        'vypis': vypis,
        'items_in_shop': items_in_shop,
    }

    return redirect(reverse('shop-url'))

def shop_buy(request, item_id):
    print(f"Spuštění funkce nákupu položky: {item_id}")
    user = request.user
    item_to_buy = ShopOffer.objects.get(item_id=item_id)
    economy = Economy.objects.get(hrac=user)

    if economy.gold >= item_to_buy.price:

        buy_or_sell(request, 'gold', item_to_buy.price, 'minus')

        INV.objects.create(
            hrac=user,
            item_id=item_to_buy.item_id,
            name=item_to_buy.name,
            img_init=item_to_buy.img_init,
            description=item_to_buy.description,
            level_required=item_to_buy.level_required,
            level_stop=item_to_buy.level_stop,
            item_type=item_to_buy.item_type,
            item_category=item_to_buy.item_category,
            slots=item_to_buy.slots,
            price=item_to_buy.price,
            sell_price=item_to_buy.sell_price,
            min_dmg=item_to_buy.min_dmg,
            max_dmg=item_to_buy.max_dmg,
            prum_dmg=item_to_buy.prum_dmg,
            armor=item_to_buy.armor,
            str_bonus=item_to_buy.str_bonus,
            dex_bonus=item_to_buy.dex_bonus,
            int_bonus=item_to_buy.int_bonus,
            vit_bonus=item_to_buy.vit_bonus,
            luk_bonus=item_to_buy.luk_bonus,
            kriticke_poskozeni_procenta_it_bonus=item_to_buy.kriticke_poskozeni_procenta_it_bonus,
            sance_na_bezvedomi_procenta_it_bonus=item_to_buy.sance_na_bezvedomi_procenta_it_bonus,
            sance_na_otravu_procenta_it_bonus=item_to_buy.sance_na_otravu_procenta_it_bonus,
            poskozeni_utokem_procenta_it_bonus=item_to_buy.poskozeni_utokem_procenta_it_bonus,
            poskozeni_schopnosti_procenta_it_bonus=item_to_buy.poskozeni_schopnosti_procenta_it_bonus,
            pvp_poskozeni_procenta_it_bonus=item_to_buy.pvp_poskozeni_procenta_it_bonus,
            pvm_poskozeni_procenta_it_bonus=item_to_buy.pvm_poskozeni_procenta_it_bonus,
            str_flat_it_bonus=item_to_buy.str_flat_it_bonus,
            dex_flat_it_bonus=item_to_buy.dex_flat_it_bonus,
            int_flat_it_bonus=item_to_buy.int_flat_it_bonus,
            vit_flat_it_bonus=item_to_buy.vit_flat_it_bonus,
            luck_flat_it_bonus=item_to_buy.luck_flat_it_bonus,
            bezvedomi_resist_procenta_it_bonus=item_to_buy.bezvedomi_resist_procenta_it_bonus,
            otrava_resist_procenta_it_bonus=item_to_buy.otrava_resist_procenta_it_bonus,
            light_resist_procenta_it_bonus=item_to_buy.light_resist_procenta_it_bonus,
            heavy_resist_procenta_it_bonus=item_to_buy.heavy_resist_procenta_it_bonus,
            magic_resist_procenta_it_bonus=item_to_buy.magic_resist_procenta_it_bonus,
            pvp_resist_procenta_it_bonus=item_to_buy.pvp_resist_procenta_it_bonus,
            pvm_resist_procenta_it_bonus=item_to_buy.pvm_resist_procenta_it_bonus,
            hp_flat_it_bonus=item_to_buy.hp_flat_it_bonus
        )

        ShopOffer.objects.filter(item_id=item_id).delete()

        print(f"Nákup položky: {item_to_buy.name} za cenu {item_to_buy.price} zlaťáků")
    else:
        print(f"Nedostatek zlata na nákup položky: {item_to_buy.name}")

    return redirect(reverse('shop-url'))
