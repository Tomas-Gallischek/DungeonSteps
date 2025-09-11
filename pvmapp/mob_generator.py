import random
from .models import Mobs
import random

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
    
    name = random.choice(monster_names)
    mob_id = random.randint(1000, 99999)
    dificulty_koeficient = random.randint(1, 5)
    mob_lvl = random.randint(1, 20)

    dmg_atr = random.choice([choice[0] for choice in ATRIBUTS_CHOICES if choice[0] != 'none'])


    str = (random.randint(1, 10) * dificulty_koeficient) * mob_lvl
    if dmg_atr == 'strength':
        str = str + (str * 2)
    dex = (random.randint(1, 10) * dificulty_koeficient) * mob_lvl
    if dmg_atr == 'dexterity':
        dex = dex + (dex * 2)
    int = (random.randint(1, 10) * dificulty_koeficient) * mob_lvl
    if dmg_atr == 'intelligence':
        int = int + (int * 2)
    vit = (random.randint(1, 20) * dificulty_koeficient) * mob_lvl
    luck = (random.randint(1, 10) * dificulty_koeficient) * mob_lvl

    hp = ((100 + (vit * 5)) * dificulty_koeficient) * mob_lvl


    magic_resist = 1 + ( (random.randint(1, 50)) / 100 )
    light_resist = 1 + ( (random.randint(1, 50)) / 100 )
    heavy_resist = 1 + ( (random.randint(1, 50)) / 100 )
    otrava_resist = 1 + ( (random.randint(1, 50)) / 100 )
    bezvedomi_resist = 1 + ( (random.randint(1, 50)) / 100 )

    poskozeni_schopnosti = 1 + (random.randint(1, 10) / 10)
    poskozeni_utokem = 1 + (random.randint(1, 30) / 10)
    sance_na_otravu = 1 + ( (random.randint(1, 50)) / 100 )
    sance_na_bezvedomi = 1 + ( (random.randint(1, 50)) / 100 )

    sance_na_kriticky_utok = (luck * 5 ) / mob_lvl
    kriticke_poskozeni = 1 + ( (random.randint(1, 50)) / 100 )

    armor = 50 * dificulty_koeficient * mob_lvl

    armor_normal = armor
    armor_light = (armor * light_resist)
    armor_heavy = (armor * heavy_resist)
    armor_magic = (armor * magic_resist)

    dmg_koef = mob_lvl ** dificulty_koeficient
    max_dmg_random = random.sample(range(1, 5), 1)[0]

    min_dmg = random.randint(1, dmg_koef) 
    max_dmg = min_dmg * max_dmg_random


    Mobs.objects.create(
        name=name,
        mob_id=mob_id,
        dificulty_koeficient=dificulty_koeficient,
        lvl=mob_lvl,
        hp=hp,
        str=str,
        dex=dex,
        int=int,
        vit=vit,
        luck=luck,
        dmg_atr=dmg_atr,
        magic_resist=magic_resist,
        light_resist=light_resist,
        heavy_resist=heavy_resist,
        otrava_resist=otrava_resist,
        bezvedomi_resist=bezvedomi_resist,
        poskozeni_schopnosti=poskozeni_schopnosti,
        poskozeni_utokem=poskozeni_utokem,
        sance_na_otravu=sance_na_otravu,
        sance_na_bezvedomi=sance_na_bezvedomi,
        sance_na_kriticky_utok=sance_na_kriticky_utok,
        kriticke_poskozeni=kriticke_poskozeni,
        armor=armor,
        min_dmg=min_dmg,
        max_dmg=max_dmg
    )

    print(f"Generován mob: {name}, ID: {mob_id}, Úroveň: {mob_lvl}, Síla: {str}, Obratnost: {dex}, Inteligence: {int}, Vitalita: {vit}, Štěstí: {luck}, HP: {hp}, Zbraň: {min_dmg}-{max_dmg} DMG, Atribut poškození: {dmg_atr}")
