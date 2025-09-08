from .models import EQP, XP_LVL, Atributs
import random

def off_stats(request):
# IMPORTY
    user = request.user
    rasa = user.rasa
    povolani = user.povolani
    atributy = Atributs.objects.get(hrac=user)
    equipment = EQP.objects.filter(hrac=user)
    weapon = equipment.filter(item_type='weapon')
    print(f"EQP {equipment}")
    print(f"Zbraň: {weapon}")
# VÝPOČTY
    prum_dmg = ()
# EXPORT




def def_stats(request):
    user = request.user
    rasa = user.rasa
    povolani = user.povolani
    atributy = Atributs.objects.get(hrac=user)