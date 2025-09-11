from tkinter import Place
from turtle import up
from urllib import request
from django.contrib.auth.decorators import login_required
from hracapp import models
from hracapp.models import Atributs, Playerinfo

@login_required
def rasa_povolani_bonus_create(request):
    user = request.user
    rasa = user.rasa
    povolani = user.povolani

    koeficient_statu = 3  # JEŠTĚ NEVÍM KOLIK PŘESNĚ BUDOU ZÁKLADNÍ STATY. PÍŠU TO CO BYL ORIGINÁL A PŘÍPADNĚ TO NÁSOBÍM

    print(f"generování základní statů pro rasu: {rasa} a povolání: {povolani}")

    # DODĚLAT MANU

    if rasa == 'Člověk' or rasa == 'human':
        hp_rasa = 50 * koeficient_statu
        hp_koeficient = 1.6
        strength_base = 5 * koeficient_statu
        vitality_base = 4 * koeficient_statu
        dexterity_base = 5 * koeficient_statu
        intelligence_base = 4 * koeficient_statu
        luck_base = 7 * koeficient_statu

    elif rasa == 'Elf' or rasa == 'elf':
        hp_rasa = 30 * koeficient_statu
        hp_koeficient = 1.2
        strength_base = 3 * koeficient_statu
        vitality_base = 2 * koeficient_statu
        dexterity_base = 7 * koeficient_statu
        intelligence_base = 8 * koeficient_statu
        luck_base = 5 * koeficient_statu

    elif rasa == 'Trpaslík' or rasa == 'dwarf':
        hp_rasa = 70 * koeficient_statu
        hp_koeficient = 1.8
        strength_base = 6 * koeficient_statu
        vitality_base = 8 * koeficient_statu
        dexterity_base = 3 * koeficient_statu
        intelligence_base = 3 * koeficient_statu
        luck_base = 5 * koeficient_statu

    elif rasa == 'ork' or rasa == 'ork':
        hp_rasa = 80 * koeficient_statu
        hp_koeficient = 2.0
        strength_base = 6 * koeficient_statu
        vitality_base = 10 * koeficient_statu
        dexterity_base = 2 * koeficient_statu
        intelligence_base = 2 * koeficient_statu
        luck_base = 5 * koeficient_statu

    elif rasa == 'Gnóm' or rasa == 'gnome':
        hp_rasa = 50 * koeficient_statu
        hp_koeficient = 1.4
        strength_base = 4 * koeficient_statu
        vitality_base = 4 * koeficient_statu
        dexterity_base = 5 * koeficient_statu
        intelligence_base = 6 * koeficient_statu
        luck_base = 6 * koeficient_statu

    elif rasa == 'Stín' or rasa == 'shadow':
        hp_rasa = 20 * koeficient_statu
        hp_koeficient = 1.0
        strength_base = 3 * koeficient_statu
        vitality_base = 2 * koeficient_statu
        dexterity_base = 12 * koeficient_statu
        intelligence_base = 3 * koeficient_statu
        luck_base = 5 * koeficient_statu

    else:
        print(" ! NEVYBRALA SE ŽÁDNÁ RASA !")

    if povolani == 'Hraničář' or povolani == 'ranger':
        dmg_atribut = 'dexterity'
        item_type = 'light'
    elif povolani == 'Paladin' or povolani == 'paladin':
        dmg_atribut = 'strength'
        item_type = 'heavy'
    elif povolani == 'Mág' or povolani == 'mage':
        dmg_atribut = 'intelligence'
        item_type = 'magic'
    else:
        print(" ! NEVYBRALO SE ŽÁDNÉ POVOLÁNÍ !")

    # Načtení instance a uložení upravených hodnot
    atributs_instance = Atributs.objects.get(hrac=user)
    atributs_instance.hp_koeficient = hp_koeficient
    atributs_instance.hp_rasa = hp_rasa
    atributs_instance.strength_base = strength_base
    atributs_instance.vitality_base = vitality_base
    atributs_instance.dexterity_base = dexterity_base
    atributs_instance.intelligence_base = intelligence_base
    atributs_instance.luck_base = luck_base
    atributs_instance.dmg_atribut = dmg_atribut
    Playerinfo.objects.filter(username=user.username).update(item_type=item_type)
    atributs_instance.save()
    print("Základní staty byly úspěšně vytvořeny a uloženy do databáze.")

