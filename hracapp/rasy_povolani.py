from .models import Atributs, Playerinfo
from urllib import request
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login

@login_required
def povolani_bonus(request):
    user = request.user
    print(f"Funkce povolani_bonus byla zavolána pro uživatele: {user.username}, povolání: {user.povolani}")
    atributy_hrace = Atributs.objects.filter(hrac=user)

    print (f"Zvolené povolání: {user.povolani}")
    # SÍLA (DMG -> MID -> TANK)
    if user.povolani == 'Paladin' or user.povolani == 'paladin':
        dmg_atribut = 'strength'
    elif user.povolani == 'Válečník' or user.povolani == 'warrior':
        dmg_atribut = 'strength'
    elif user.povolani == 'Ničitel' or user.povolani == 'berserker':
        dmg_atribut = 'strength'

    # INTELIGENCE (DMG -> MID -> TANK (heal))
    elif user.povolani == 'Mág' or user.povolani == 'mage':
        dmg_atribut = 'intelligence'
    elif user.povolani == 'Nekromant' or user.povolani == 'necromancer':
        dmg_atribut = 'intelligence'
    elif user.povolani == 'Druid' or user.povolani == 'druid':
        dmg_atribut = 'intelligence'

    # OBRATNOST (DMG -> MID -> TANK)
    elif user.povolani == 'Roguna' or user.povolani == 'rogue':
        dmg_atribut = 'dexterity'
    elif user.povolani == 'Hraničář' or user.povolani == 'ranger':
        dmg_atribut = 'dexterity'
    elif user.povolani == 'Mnich' or user.povolani == 'monk':
        dmg_atribut = 'dexterity'

    print(f"Zvolené povolání: {user.povolani}, DMG atribut: {dmg_atribut}")
    atributy_hrace.dmg_atribut = dmg_atribut
    Atributs.objects.filter(hrac=user).update(dmg_atribut=dmg_atribut)


@login_required
def rasa_bonus(request):

    koeficient_statu = 3  # JEŠTĚ NEVÍM KOLIK PŘESNĚ BUDOU ZÁKLADNÍ STATY. PÍŠU TO CO BYL ORIGINÁL A PŘÍPADNĚ TO NÁSOBÍM

    if request.user.rasa == 'Člověk' or request.user.rasa == 'human':
        # OBECNÉ BONUSY
        hp_bonus = 1
        # ZÁKLADNÍ STATY
        strength_bonus = 5 * koeficient_statu
        vitality_bonus = 4 * koeficient_statu
        dexterity_bonus = 4 * koeficient_statu
        intelligence_bonus = 3 * koeficient_statu
        charisma_bonus = 5 * koeficient_statu
        luck_bonus = 3 * koeficient_statu

    elif request.user.rasa == 'Elf' or request.user.rasa == 'elf':
        # OBECNÉ BONUSY
        hp_bonus = 0.8
        # ZÁKLADNÍ STATY
        strength_bonus = 3 * koeficient_statu
        vitality_bonus = 3 * koeficient_statu
        dexterity_bonus = 5 * koeficient_statu
        intelligence_bonus = 7 * koeficient_statu
        charisma_bonus = 4 * koeficient_statu
        luck_bonus = 3 * koeficient_statu

    elif request.user.rasa == 'Trpaslík' or request.user.rasa == 'dwarf':
        # OBECNÉ BONUSY
        hp_bonus = 1.2
        # ZÁKLADNÍ STATY
        strength_bonus = 4 * koeficient_statu
        vitality_bonus = 5 * koeficient_statu
        dexterity_bonus = 3 * koeficient_statu
        intelligence_bonus = 3 * koeficient_statu
        charisma_bonus = 3 * koeficient_statu
        luck_bonus = 6 * koeficient_statu

    elif request.user.rasa == 'Urgal' or request.user.rasa == 'urgal':
        # OBECNÉ BONUSY
        hp_bonus = 1.3
        # ZÁKLADNÍ STATY
        strength_bonus = 5 * koeficient_statu
        vitality_bonus = 9 * koeficient_statu
        dexterity_bonus = 3 * koeficient_statu
        intelligence_bonus = 3 * koeficient_statu
        charisma_bonus = 2 * koeficient_statu
        luck_bonus = 2 * koeficient_statu

    elif request.user.rasa == 'Gnóm' or request.user.rasa == 'gnome':
        # OBECNÉ BONUSY
        hp_bonus = 1
        # ZÁKLADNÍ STATY
        strength_bonus = 4 * koeficient_statu
        vitality_bonus = 4 * koeficient_statu
        dexterity_bonus = 4 * koeficient_statu
        intelligence_bonus = 5 * koeficient_statu
        charisma_bonus = 2 * koeficient_statu
        luck_bonus = 5 * koeficient_statu

    elif request.user.rasa == 'Stín' or request.user.rasa == 'shadow':
        # OBECNÉ BONUSY
        hp_bonus = 0.7
        # ZÁKLADNÍ STATY
        strength_bonus = 3 * koeficient_statu
        vitality_bonus = 2 * koeficient_statu
        dexterity_bonus = 10 * koeficient_statu
        intelligence_bonus = 3 * koeficient_statu
        charisma_bonus = 2 * koeficient_statu
        luck_bonus = 4 * koeficient_statu
    else:
        print(" ! NEVYBRALA SE ŽÁDNÁ RASA !")

    request.user.hp_bonus = float(hp_bonus)
    request.user.strength_base = float(strength_bonus)
    request.user.vitality_base = float(vitality_bonus)
    request.user.dexterity_base = float(dexterity_bonus)
    request.user.intelligence_base = float(intelligence_bonus)
    request.user.charisma_base = float(charisma_bonus)
    request.user.luck_base = float(luck_bonus)
    request.user.save()

    rasa_bonus = (
        hp_bonus + strength_bonus + vitality_bonus + dexterity_bonus + intelligence_bonus + charisma_bonus + luck_bonus
    )
    return rasa_bonus