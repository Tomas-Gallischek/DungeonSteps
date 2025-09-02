import os
import django
import sys
import random
if __name__ == "__main__": # <-- KÓD PRO SPRÁVNÉ SPUŠTĚNÍ PŘI TESTOVÁNÍ FUNKCE
    # Nastavení Django prostředí
    # Zde se ujistíte, že je správná cesta k projektu na Python path
    current_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(current_dir)
    sys.path.append(project_root)

    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'houska.settings')
    django.setup()

from itemsapp.models import Weapons
img_init = 1
level_required = 1

types = ['heavy', 'light', 'ranged']
GREEN = '\033[92m'

test_weapons_list = [
    "Dřevěný meč",
    "Rezavý tesák",
    "Kamenná sekyra",
    "Kopí dráteníka",
    "Štít z borovice",
    "Křehký luk",
    "Bojový cep",
    "Meč železného kováře",
    "Rychlý dýka",
    "Kopí vesničana",
    "Ocelový meč",
    "Dlouhá sekyra",
    "Meč strážce",
    "Ostrá šavle",
    "Štít rytíře",
    "Rytířský meč",
    "Kožený bič",
    "Kopí dračího jezdce",
    "Ocelový luk",
    "Sekera řezníka",
    "Oheň osudu",
    "Meč ohnivého stínu",
    "Hněv hromu",
    "Šíp věčného stínu",
    "Krvavý dráp",
    "Kladivo ohnivého trpaslíka",
    "Pád hvězd",
    "Sekyra krále",
    "Záblesk úsvitu",
    "Stříbrná šavle",
    "Korupce",
    "Osud",
    "Krvavé ostří",
    "Sekera z kamene srdce",
    "Volání prázdnoty",
    "Věčný plamen",
    "Drakobijce",
    "Hlas přírody",
    "Sekyra stínového rytíře",
    "Kladivo dračího srdce",
    "Meč osudového trůnu",
    "Vládce krve",
    "Poslední naděje",
    "Zářící úsvit",
    "Královo ostří",
    "Poslední pramen",
    "Krvavá bouře",
    "Kladivo osudného dne",
    "Zničení reality",
    "Věčnost a smrt"
]

for one in test_weapons_list:
    new_weapon = Weapons()
    new_weapon.img_init = img_init
    img_init += 1
    new_weapon.name = one
    new_weapon.type = random.choice(types)
    new_weapon.level_required = level_required
    level_required += 1
    new_weapon.level_stop = 5 + level_required
    new_weapon.description = f"Popis zbraně {one} - TEST ZBRAŇ"
    new_weapon.save()
    print(f"{GREEN}Zbraň {one} byla ULOŽENA DO DATABÁZE")
    print(f"  Požadovaná úroveň: {new_weapon.level_required}")
    print(f"  Zastavovací úroveň: {new_weapon.level_stop}")

print(f"{GREEN}Testovací zbraně byly vytvořeny")