from .full_shop import full_shop
from django.shortcuts import render
from hracapp.models import ShopOffer
from django.contrib.auth.decorators import login_required

@login_required
def shop(request):
    print(f"Spuštění funkce renderování obchodu")
    user = request.user
    vypis = full_shop(request)
    items_in_shop = ShopOffer.objects.all()
    context = {
        'user': user,
        'vypis': vypis,
        'items_in_shop': items_in_shop,
    }

    return render(request, 'shopapp/shop.html', context)

