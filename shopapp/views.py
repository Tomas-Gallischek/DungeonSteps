from .full_shop import full_shop
from django.shortcuts import redirect, render
from hracapp.models import ShopOffer
from django.contrib.auth.decorators import login_required

@login_required
def shop(request):
    print(f"Spuštění funkce renderování obchodu")

    items_in_shop = ShopOffer.objects.all()
    if items_in_shop == None:
        vypis = shop_reset(request)
        context = {
            'items_in_shop': items_in_shop,
            'vypis': vypis,
            'user': request.user,
        }
        return render(request, 'shopapp/shop.html', context)
    else:
        return render(request, 'shopapp/shop.html')

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

    return render(request, 'shopapp/shop.html', context)

