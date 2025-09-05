import re
from django.shortcuts import redirect
from .models import Economy, Economy_Log


def buy_or_sell_convert(request):
    if request.method == "POST":
        currency_type = request.POST.get("currency_type")
        amount = request.POST.get("amount")
        amount = int(amount) if amount else 0
        operation = request.POST.get("operation")
        return buy_or_sell(request, currency_type, amount, operation)
    if currency_type and amount and operation:
        return buy_or_sell(request, currency_type, amount, operation)

def buy_or_sell(request, currency_type, amount, operation):

    user = request.user
    economy = Economy.objects.get(hrac=user)
    
    # Určí správnou hodnotu pro transakci na základě operace
    if operation == 'minus':
        transaction_amount = -abs(amount)
    elif operation == 'plus':
        transaction_amount = abs(amount)
    else:
        raise ValueError("Neplatná operace. Použijte 'plus' nebo 'minus'.")
    
    # Aktualizuje hodnoty a loguje transakci
    if currency_type == 'gold':
        economy.gold += transaction_amount
        log_data = {'gold_change': transaction_amount}
    elif currency_type == 'dungeon_token':
        economy.dungeon_token += transaction_amount
        log_data = {'dungeon_token_change': transaction_amount}
    else:
        raise ValueError("Neplatný typ měny. Použijte 'gold' nebo 'dungeon_token'.")

    # Uloží změny a zaloguje transakci
    economy.save()
    Economy_Log.objects.create(hrac=user, **log_data)

    return redirect('profile-url')