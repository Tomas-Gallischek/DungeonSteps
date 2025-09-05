from turtle import up
from urllib import request
from django.contrib.auth.decorators import login_required
from hracapp import models
from hracapp.models import Atributs

@login_required
def rasa_bonus_create(request):
    user = request.user
    rasa = user.rasa

    koeficient_statu = 3  # JEŠTĚ NEVÍM KOLIK PŘESNĚ BUDOU ZÁKLADNÍ STATY. PÍŠU TO CO BYL ORIGINÁL A PŘÍPADNĚ TO NÁSOBÍM

    print(f"generování základní statů pro rasu: {rasa}")

    if rasa == 'Člověk' or rasa == 'human':
        hp_base = 50 * koeficient_statu
        strength_base = 4 * koeficient_statu
        vitality_base = 3 * koeficient_statu
        dexterity_base = 4 * koeficient_statu
        intelligence_base = 3 * koeficient_statu
        charisma_base = 5 * koeficient_statu
        luck_base = 5 * koeficient_statu

    elif rasa == 'Elf' or rasa == 'elf':
            hp_base = 30 * koeficient_statu
            strength_base = 3 * koeficient_statu
            vitality_base = 2 * koeficient_statu
            dexterity_base = 5 * koeficient_statu
            intelligence_base = 6 * koeficient_statu
            charisma_base = 4 * koeficient_statu
            luck_base = 5 * koeficient_statu

    elif rasa == 'Trpaslík' or rasa == 'dwarf':
            hp_base = 70 * koeficient_statu
            strength_base = 4 * koeficient_statu
            vitality_base = 6 * koeficient_statu
            dexterity_base = 3 * koeficient_statu
            intelligence_base = 3 * koeficient_statu
            charisma_base = 3 * koeficient_statu
            luck_base = 5 * koeficient_statu

    elif rasa == 'Urgal' or rasa == 'urgal':
        hp_base = 80 * koeficient_statu
        strength_base = 5 * koeficient_statu
        vitality_base = 8 * koeficient_statu
        dexterity_base = 2 * koeficient_statu
        intelligence_base = 2 * koeficient_statu
        charisma_base = 2 * koeficient_statu
        luck_base = 5 * koeficient_statu


    elif rasa == 'Gnóm' or rasa == 'gnome':
        hp_base = 50 * koeficient_statu
        strength_base = 4 * koeficient_statu
        vitality_base = 4 * koeficient_statu
        dexterity_base = 4 * koeficient_statu
        intelligence_base = 5 * koeficient_statu
        charisma_base = 2 * koeficient_statu
        luck_base = 5 * koeficient_statu


    elif rasa == 'Stín' or rasa == 'shadow':
        hp_base = 20 * koeficient_statu
        strength_base = 3 * koeficient_statu
        vitality_base = 2 * koeficient_statu
        dexterity_base = 9 * koeficient_statu
        intelligence_base = 3 * koeficient_statu
        charisma_base = 2 * koeficient_statu
        luck_base = 5 * koeficient_statu

    else:
        print(" ! NEVYBRALA SE ŽÁDNÁ RASA !")

    print(f"Základní staty pro rasu {rasa} jsou: hp: {hp_base}, str: {strength_base}, vit: {vitality_base}, dex: {dexterity_base}, int: {intelligence_base}, cha: {charisma_base}, luc: {luck_base}")

    Atributs.objects.filter(hrac=user).update(
        hp_base=hp_base,
        strength_base=strength_base,
        vitality_base=vitality_base,
        dexterity_base=dexterity_base,
        intelligence_base=intelligence_base,
        charisma_base=charisma_base,
        luck_base=luck_base
    )
