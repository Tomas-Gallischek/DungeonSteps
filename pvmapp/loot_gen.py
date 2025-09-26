from hracapp.xp_lvl import xp_plus
from hracapp.economy import buy_or_sell
import random


def loot_gen(request, mob):

# VYGENEROVÁNÍ ZÍSKANÝCH XP
    base_xp_loot = mob['lvl'] * mob['dificulty_koeficient'] * 10
    xp_bonus = 1 + (random.randint(1, 20) / 100)  # max 1.2 (= +20% XP)
    base_xp_loot *= xp_bonus

# VYGENEROVÁNÍ ZÍSKANÝCH GOLDŮ
    base_gold_loot = mob['lvl'] * mob['dificulty_koeficient']
    gold_bonus = 1 + (random.randint(1, 20) / 100)  # max 1.5 (= +50% gold)
    base_gold_loot *= gold_bonus

# SPŮŠTĚNÍ FUNKCE PRO ZÁPIS LOOTU DO DATABÁZE
    buy_or_sell(request, 'gold', round(base_gold_loot), 'plus')
    xp_plus(request, round(base_xp_loot), 'plus')



# RETURN
    loot = {
        'xp': round(base_xp_loot),
        'gold': round(base_gold_loot),
    }

    return loot