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
            slot_1_bonus=item_to_buy.slot_1_bonus,
            slot_1_value=item_to_buy.slot_1_value,
            slot_2_bonus=item_to_buy.slot_2_bonus,
            slot_2_value=item_to_buy.slot_2_value,
            slot_3_bonus=item_to_buy.slot_3_bonus,
            slot_3_value=item_to_buy.slot_3_value,
            slot_4_bonus=item_to_buy.slot_4_bonus,
            slot_4_value=item_to_buy.slot_4_value,
            price=item_to_buy.price,
            min_dmg=item_to_buy.min_dmg,
            max_dmg=item_to_buy.max_dmg,
            prum_dmg=item_to_buy.prum_dmg,
            armor=item_to_buy.armor,
            str_bonus=item_to_buy.str_bonus,
            dex_bonus=item_to_buy.dex_bonus,
            int_bonus=item_to_buy.int_bonus,
            vit_bonus=item_to_buy.vit_bonus,
            luk_bonus=item_to_buy.luk_bonus,
        )

        ShopOffer.objects.filter(item_id=item_id).delete()

        print(f"Nákup položky: {item_to_buy.name} za cenu {item_to_buy.price} zlaťáků")
    else:
        print(f"Nedostatek zlata na nákup položky: {item_to_buy.name}")

    return redirect(reverse('shop-url'))
