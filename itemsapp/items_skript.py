import os
from re import I
import django
import sys
import random
import string

if __name__ == "__main__": # <-- KÓD PRO SPRÁVNÉ SPUŠTĚNÍ PŘI TESTOVÁNÍ FUNKCE
    # Nastavení Django prostředí
    # Zde se ujistíte, že je správná cesta k projektu na Python path
    current_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(current_dir)
    sys.path.append(project_root)

    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'houska.settings')
    django.setup()

# SKRIPT
item_list = [f"item{i}" for i in range(1, 100)]
item_categories = ['weapon', 'armor', 'helmet', 'boots', 'ring', 'amulet', 'talisman']
item_types_weapons = ['universal', 'heavy', 'light', 'magic']
item_types_armor_helmet = ['heavy', 'light', 'magic']
item_types_other = ['universal']

for one_item in item_list:
    category = random.choice(item_categories)
    if category == 'weapon':
        type = random.choice(item_types_weapons)
    elif category in ['armor', 'helmet']:
        type = random.choice(item_types_armor_helmet)
    else:
        type = random.choice(item_types_other)

    name = one_item

    id = ""
    for i in range(10):
        random_pismeno = random.choice(string.ascii_letters)
        random_cislo = random.randint(1, 100)
        id += f"{random_pismeno}{random_cislo}"

    description = f"Popis předmětu {one_item}"

    level_required = random.randint(1, 20)
    level_stop = level_required + random.randint(5, 20)

# VŠECHNO OSTATNÍ SE GENERUJE AŽ V OBCHODĚ KVŮLI LEVELU HRÁČE
    
    from itemsapp.models import Items

    Items.objects.create(
        name = name,
        item_id = id,
        img_init = f"images/items/{id}.png",
        description = description,
        level_required = level_required,
        level_stop = level_stop,
        item_type = type,
        item_category = category,

        slots = 0,
        slot_1_bonus = "",
        slot_1_value = 0,
        slot_2_bonus = "",
        slot_2_value = 0,
        slot_3_bonus = "",
        slot_3_value = 0,
        slot_4_bonus = "",
        slot_4_value = 0,

        price = 0,

        min_dmg = 0,
        max_dmg = 1,
        prum_dmg = 0.0,

        armor = 0,

        str_bonus = 0,
        dex_bonus = 0,
        int_bonus = 0,
        vit_bonus = 0,
        luk_bonus = 0
    )

    print(f"Předmět {one_item} vytvořen.")

