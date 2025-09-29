from os import error
from pickle import TRUE
from django.http import HttpRequest
from django.http import HttpResponse
from django.shortcuts import redirect
from .models import Economy, Economy_Log, INV
from django.contrib import messages

def sell_item(request, item_id):
    print(f"Selling item with ID: {item_id}")
    user = request.user
    economy = Economy.objects.get(hrac=user)
    item = INV.objects.filter(hrac=user, item_id=item_id).first()

    if item:

        request, currency_type, amount, operation = request, 'gold', item.sell_price, 'plus'
        buy_or_sell(request, currency_type, amount, operation)

        item.delete()  # Odstranění položky z inventáře
        print(f"Item with ID: {item_id} sold for {item.sell_price} gold.")
    else:
        print(f"Item with ID: {item_id} not found in inventory.")
        return redirect('profile-url')  # Nebo jiná vhodná reakce na neexistující položku
    

    return redirect('profile-url')


def buy_or_sell_convert(request):
    if request.method == "POST":
        currency_type = request.POST.get("currency_type")
        amount = request.POST.get("amount")
        amount = int(amount) if amount else 0
        operation = request.POST.get("operation")

        buy_or_sell(request, currency_type, amount, operation)

    return redirect('profile-url')


def buy_or_sell(request, currency_type, amount, operation):
    user = request.user
    economy = Economy.objects.get(hrac=user)
    
    if amount > economy.gold and operation == 'minus':
        # Nedostatek zlatých na odečtení
        print("Nedostatek zlatých na odečtení.")
        messages.error(request, "Nedostatek goldů")
        return redirect('profile-url')

    else:
        print(f"Processing {operation} of {amount} {currency_type} for user {user.username}")
        # Určí správnou hodnotu pro transakci na základě operace
        if operation == 'minus':
            transaction_amount = -abs(amount)
        elif operation == 'plus':
            transaction_amount = abs(amount)
    
        # Aktualizuje hodnoty a loguje transakci
        if currency_type == 'gold':
            economy.gold += transaction_amount
            log_data = {'gold_change': transaction_amount}
        elif currency_type == 'dungeon_token':
            economy.dungeon_token += transaction_amount
            log_data = {'dungeon_token_change': transaction_amount}


        print(f"{transaction_amount} {currency_type} for user {user.username}")
        # Uloží změny a zaloguje transakci
        economy.save()
        Economy_Log.objects.create(hrac=user, **log_data)
