from locale import currency
from django.shortcuts import redirect, render
from django.urls import reverse

from.economy import buy_or_sell
from .models import Playerinfo, Atributs

def atr_update(request):
    user = request.user
    atributy_model = Atributs.objects.get(hrac=user)
    if request.method == "POST":
        attribute = request.POST.get("attribute")
        if attribute == "strength":
            amount = atributy_model.strength_cena
            currency_type = 'gold'
            operation = 'minus'
            buy_or_sell(request, currency_type, amount, operation)
            atributy_model.strength_plus += 1
        elif attribute == "dexterity":
            amount = atributy_model.dexterity_cena
            currency_type = 'gold'
            operation = 'minus'
            buy_or_sell(request, currency_type, amount, operation)
            atributy_model.dexterity_plus += 1
        elif attribute == "intelligence":
            amount = atributy_model.intelligence_cena
            currency_type = 'gold'
            operation = 'minus'
            buy_or_sell(request, currency_type, amount, operation)
            atributy_model.intelligence_plus += 1
        elif attribute == "charisma":
            amount = atributy_model.charisma_cena
            currency_type = 'gold'
            operation = 'minus'
            buy_or_sell(request, currency_type, amount, operation)
            atributy_model.charisma_plus += 1
        elif attribute == "vitality":
            amount = atributy_model.vitality_cena
            currency_type = 'gold'
            operation = 'minus'
            buy_or_sell(request, currency_type, amount, operation)
            atributy_model.vitality_plus += 1
        elif attribute == "luck":
            amount = atributy_model.luck_cena
            currency_type = 'gold'
            operation = 'minus'
            buy_or_sell(request, currency_type, amount, operation)
            atributy_model.luck_plus += 1
        atributy_model.save()

    return redirect(reverse('profile-url'))
