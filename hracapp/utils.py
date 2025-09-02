from django.contrib.auth.decorators import login_required
from django.utils import timezone

@login_required
def atributy_hodnota(request):
    user = request.user
    user = user.atributy

    # ŽIVOTY
    base_hp = 10
    hp_bonus_rasa = user.hp_bonus
    hp_bonus_vitality = user.suma_vitality * 0.1
    plus_hp = 1 * hp_bonus_rasa * hp_bonus_vitality
    suma_hp = (base_hp * hp_bonus_rasa) * ((100 + hp_bonus_vitality)/100)

    # URČENÍ ZÁKLADNÍCH ATRIBUTŮ a jejich zpětné uložení (nic se nemění)
    base_strength = user.strength_base
    base_dexterity = user.dexterity_base
    base_intelligence = user.intelligence_base
    base_charisma = user.charisma_base
    base_vitality = user.vitality_base
    base_luck = user.luck_base
    user.save()

    # URČENÍ A ULOŽENÍ HODNOTY ATRIBUTŮ (plus)
    plus_strength = user.strength_plus
    plus_dexterity = user.dexterity_plus
    plus_intelligence = user.intelligence_plus
    plus_charisma = user.charisma_plus
    plus_vitality = user.vitality_plus
    plus_luck = user.luck_plus
    user.save()

    # DEFINITIVNÍ HODNOTA ATRIBUTŮ (základ + hodnota v databázi)

    suma_strength = base_strength + plus_strength
    suma_dexterity = base_dexterity + plus_dexterity
    suma_intelligence = base_intelligence + plus_intelligence
    suma_charisma = base_charisma + plus_charisma
    suma_vitality = base_vitality + plus_vitality
    suma_luck = base_luck + plus_luck
    user.suma_strength = suma_strength
    user.suma_dexterity = suma_dexterity
    user.suma_intelligence = suma_intelligence
    user.suma_charisma = suma_charisma
    user.suma_vitality = suma_vitality
    user.suma_luck = suma_luck
    user.save()

    base_atributy = {
        "base_hp": int(base_hp),
        "base_strength": int(base_strength),
        "base_dexterity": int(base_dexterity),
        "base_intelligence": int(base_intelligence),
        "base_charisma": int(base_charisma),
        "base_vitality": int(base_vitality),
        "base_luck": int(base_luck)
    }

    plus_atributy = {
        "plus_hp": int(plus_hp),
        "plus_strength": int(plus_strength),
        "plus_dexterity": int(plus_dexterity),
        "plus_intelligence": int(plus_intelligence),
        "plus_charisma": int(plus_charisma),
        "plus_vitality": int(plus_vitality),
        "plus_luck": int(plus_luck)
    }

    suma_atributy = {
        "suma_hp":  int(suma_hp),
        "suma_strength":  int(suma_strength),
        "suma_dexterity": int(suma_dexterity),
        "suma_intelligence": int(suma_intelligence),
        "suma_charisma": int(suma_charisma),
        "suma_vitality": int(suma_vitality),
        "suma_luck": int(suma_luck)
    }

    return hp_bonus_vitality, suma_atributy, base_atributy, plus_atributy, plus_strength, plus_dexterity, plus_intelligence, plus_charisma, plus_vitality, plus_luck

@login_required
def atributy_cena(request):

    hp_bonus_vitality, suma_atributy, base_atributy, plus_atributy, plus_strength, plus_dexterity, plus_intelligence, plus_charisma, plus_vitality, plus_luck = atributy_hodnota(request)


    strength_cost = 1 + (plus_strength*2)
    dexterity_cost = 1 + (plus_dexterity*2)
    intelligence_cost = 1 + (plus_intelligence*2)
    vitality_cost = 1 + (plus_vitality*2)
    luck_cost = 1 + (plus_luck*2)
    charisma_cost = 1 + (plus_charisma*2)

    atributy_cost = {
        "strength_cost":  round(strength_cost, 1),
        "dexterity_cost":  round(dexterity_cost, 1),
        "intelligence_cost":  round(intelligence_cost, 1),
        "charisma_cost":  round(charisma_cost, 1),
        "vitality_cost":  round(vitality_cost, 1),
        "luck_cost":  round(luck_cost, 1),
    }

    return atributy_cost


def calculate_xp_and_level(request):
    user = request.user
    steps = user.steps if user.steps is not None else 0
    XP_aktual = steps
    lvl_aktual = 1
    lvl_next = 2
    XP_potrebne_next = round((22 * lvl_aktual) * ((lvl_next) * 1.1))

    for lvl in range(1, 500):
        XP_potrebne = round((22 * lvl) * ((lvl**1.1)))
        if XP_aktual >= XP_potrebne:
            XP_aktual -= XP_potrebne
            lvl_aktual += 1
            lvl_next = lvl_aktual + 1
            XP_potrebne_next = round((22 * lvl_next) * ((lvl_next**1.1)))
        else:
            user.xp = XP_aktual
            user.lvl = lvl_aktual
            user.save()
            break

    return XP_aktual, lvl_aktual, lvl_next, XP_potrebne_next


def calculate_gold(request):
    user = request.user
    user_lvl = user.xp_lvl
    user_gold = user.economy
# PRVNĚ SE MUSÍ ZJISTIT JESTLI HRÁČ UŽ JE REGISTROVANÝ NEBO NE. POKUD NENÍ, MUSÍ SE MU VYTVOŘIT ZÁZNAM V DATABÁZI
    if user_lvl is None:
        user_lvl = user.xp_lvl.create(lvl=1, xp=0)
        user_lvl.save()
    else:
        user_lvl = user.xp_lvl

    if user_gold is None:
        user_gold = user.economy.create(gold=0, rohlik=0, gold_growth_coefficient=0.1, last_gold_collection=timezone.now())
        user_gold.save()
    else:
        user_gold = user.economy

    user_gold_update = 0.1 + (user_lvl.lvl * 0.1)

    if user_gold.gold_growth_coefficient != user_gold_update:
        user_gold.gold_growth_coefficient = user_gold_update
        user_gold.save()
    

    # VÝPOČET NASBÍRANÝCH GOLDŮ
    time_since_last_collection = timezone.now() - user_gold.last_gold_collection
    seconds_since_last_collection = time_since_last_collection.total_seconds()

    collected_gold = min(int(seconds_since_last_collection), 28800) * user_gold.gold_growth_coefficient
    gold_per_hour = round(user_gold.gold_growth_coefficient * 3600)
    gold_limit = gold_per_hour * 8  # Limit pro zobrazení

    user_gold.save()
    return round(collected_gold, 2), round(user_gold.gold_growth_coefficient, 2), round(gold_limit, 2), round(gold_per_hour, 2)