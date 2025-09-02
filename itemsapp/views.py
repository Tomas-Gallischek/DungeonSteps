from sys import path
from django.shortcuts import render


# FUNKCE NIC NEDĚLÁ, ALE BEZ JEJÍHO VYTVOŘENÍ MI NEŠEL SPUSTIT SERVER
def items(request):
    return render(request, 'items.html')