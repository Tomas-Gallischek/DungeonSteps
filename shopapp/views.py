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
    item_to_buy = ShopOffer.objects.get(id=item_id)
    gold_bill = item_to_buy.item_price
    economy = Economy.objects.get(hrac=user)
    golds_before = economy.gold

    if economy.gold >= item_to_buy.item_price:

        buy_or_sell(request, 'gold', item_to_buy.item_price, 'minus')

        INV.objects.create(
            hrac=item_to_buy.hrac,
            item_id=item_to_buy.item_id,
            item_type=item_to_buy.item_type,
            item_name=item_to_buy.item_name,
            item_price=item_to_buy.item_price,
            item_description=item_to_buy.item_description,
            item_level_required=item_to_buy.item_level_required,
            item_level_stop=item_to_buy.item_level_stop,
            item_weapon_type=item_to_buy.item_weapon_type,
            item_base_damage=item_to_buy.item_base_damage,
            item_min_damage=item_to_buy.item_min_damage,
            item_max_damage=item_to_buy.item_max_damage,
            item_slots=item_to_buy.item_slots
        )

        ShopOffer.objects.filter(id=item_id).delete()
        
        print(f"Nákup položky: {item_to_buy.item_name} za cenu {item_to_buy.item_price} zlaťáků")


    else:
        print(f"Nedostatek zlata na nákup položky: {item_to_buy.item_name}")

    golds_after = economy.gold


    
    print(f"Zlato před nákupem: {golds_before}, Zlato po nákupu: {golds_after}")
    return redirect(reverse('shop-url'))
