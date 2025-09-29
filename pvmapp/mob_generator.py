import random
from .models import Mobs_random
import random
from hracapp.models import XP_LVL

ATRIBUTS_CHOICES = (
    ('strength', 'Síla'),
    ('dexterity', 'Obratnost'),
    ('intelligence', 'Inteligence'),
)

monster_names = [
    "Azraelith",
    "Grimfang",
    "Goremaw",
    "Voidspawn",
    "Dreadfiend",
    "Shadowlurker",
    "Blightghoul",
    "Venomfang",
    "Skitterbeast",
    "Riftwalker",
    "Stonehide",
    "Mudslug",
    "Wailwraith",
    "Bloodgazer",
    "Cinderling",
    "Frostbite",
    "Fungusfiend",
    "Glimmerwing",
    "Ironclad",
    "Mindshriek",
    "Gloomstalker",
    "Quakebeast",
    "Screechbat",
    "Thornhide",
    "Vexling",
    "Corruptor",
    "Driftgeist",
    "Embergeist",
    "Featherghast",
    "Gravelord",
    "Hexspinner",
    "Juggernaut",
    "Kaelith",
    "Lichlord",
    "Marrowfiend",
    "Necrofang",
    "Onyxbeast",
    "Pitstalker",
    "Ruinwing",
    "Slimefang",
    "Tidecaller",
    "Umbralith",
    "Viperion",
    "Whisperling",
    "Wyrmkin",
    "Xylomancer",
    "Zephyrwing",
    "Gloomfang",
    "Cragbeast",
    "Tanglebeast"
]

def mob_gen(request):
    user = request.user
    user_lvl = XP_LVL.objects.get(hrac=user).lvl
    name = random.choice(monster_names)
    mob_id = random.randint(1000, 99999)
    dificulty_koeficient = random.uniform(1, 3)

    if user_lvl >= 6:
        mob_lvl_minus = round(user_lvl * 0.9)
        mob_lvl_plus = round(user_lvl * 1.1)
        if mob_lvl_minus == mob_lvl_plus:
            mob_lvl_plus += 1
        mob_lvl = random.randint(mob_lvl_minus, mob_lvl_plus)
    else:
        mob_lvl = user_lvl


    dmg_atr = random.choice([choice[0] for choice in ATRIBUTS_CHOICES if choice[0] != 'none'])

    str = round((random.randint(1, 5) * dificulty_koeficient) * mob_lvl)    
    if dmg_atr == 'strength':
        str = str + (str * 2)
    dex = round((random.randint(1, 5) * dificulty_koeficient) * mob_lvl)    
    if dmg_atr == 'dexterity':
        dex = dex + (dex * 2)
    int = round((random.randint(1, 5) * dificulty_koeficient) * mob_lvl)    
    if dmg_atr == 'intelligence':
        int = int + (int * 2)
    vit = round((random.randint(1, 10) * dificulty_koeficient) * mob_lvl)
    luck = round((random.randint(1, 5) * dificulty_koeficient) * mob_lvl)   

    hp = round(((100 + (vit * 5)) * dificulty_koeficient) * round(mob_lvl/2))
    if hp <= 100:
        hp = 100

    magic_resist = 1 + ( (random.randint(1, 50)) / 100 )
    light_resist = 1 + ( (random.randint(1, 50)) / 100 )
    heavy_resist = 1 + ( (random.randint(1, 50)) / 100 )
    otrava_resist = 1 + ( (random.randint(1, 50)) / 100 )
    bezvedomi_resist = 1 + ( (random.randint(1, 50)) / 100 )

    poskozeni_schopnosti = 1 + (random.randint(1, 20) / 100) # max 1.2 (= +20% dmg schopností)
    poskozeni_utokem = 1 + (random.randint(1, 40) / 100) # max 1.4 (= +40% dmg)
    sance_na_otravu = 1 + ( (random.randint(1, 50)) / 100 )
    sance_na_bezvedomi = 1 + ( (random.randint(1, 50)) / 100 )

    sance_na_kriticky_utok = (luck * 5 ) / mob_lvl
    if sance_na_kriticky_utok > 50:
        sance_na_kriticky_utok = 50
    kriticke_poskozeni = 2 + ( (random.randint(1, 50)) / 100 )

    armor = round(5 * dificulty_koeficient * (mob_lvl))

    dmg_koef = round(mob_lvl * dificulty_koeficient)
    if dmg_koef <= 1:
        dmg_koef = 2
    max_dmg_random = random.sample(range(1, 3), 1)[0]

    min_dmg = random.randint(1, dmg_koef) 
    max_dmg = (min_dmg * max_dmg_random) + dificulty_koeficient #Kdyby byl max_dmg_random 1 


    mob = {
        'name': name,
        'mob_id': mob_id,
        'dificulty_koeficient': dificulty_koeficient,
        'lvl': mob_lvl,
        'hp': hp,
        'str': str,
        'dex': dex,
        'int': int,
        'vit': vit,
        'luck': luck,
        'dmg_atr': dmg_atr,
        'magic_resist': magic_resist,
        'light_resist': light_resist,
        'heavy_resist': heavy_resist,
        'otrava_resist': otrava_resist,
        'bezvedomi_resist': bezvedomi_resist,
        'poskozeni_schopnosti': poskozeni_schopnosti,
        'poskozeni_utokem': poskozeni_utokem,
        'sance_na_otravu': sance_na_otravu,
        'sance_na_bezvedomi': sance_na_bezvedomi,
        'sance_na_kriticky_utok': sance_na_kriticky_utok,
        'kriticke_poskozeni': kriticke_poskozeni,
        'armor': armor,
        'min_dmg': min_dmg,
        'max_dmg': max_dmg
    }

    print(f"Generován mob: {name}, ID: {mob_id}, OBTÍŽNOST: {dificulty_koeficient}, Úroveň: {mob_lvl}, Síla: {str}, Obratnost: {dex}, Inteligence: {int}, Vitalita: {vit}, Štěstí: {luck}, HP: {hp}, Zbraň: {min_dmg}-{max_dmg} DMG, Atribut poškození: {dmg_atr}")

    return mob