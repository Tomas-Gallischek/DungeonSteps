from calendar import c
from math import log
import time
from django.shortcuts import render
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Mobs_dungeons
from hracapp. models import FightLogEntry, Fight, Dungeon_progress
from .mob_generator import mob_gen
from .pvm_fight import pvm_fight_funkce
from .loot_gen import loot_gen


@login_required
def dungeon_mob_fight(request):
    user = request.user

    if request.method == 'POST':
        mob_id = request.POST.get('mob_id')
        mob_id = int(mob_id) if mob_id else "špatný formát id"
        print(f"Mob ID: {mob_id}")
    if mob_id is None:
        return redirect('dungeon_map.html')
    
# NA ROZDÍL OD NÁHODNÉ MOBKY SE TADY NEMUSÍ SPUŠTĚT GENERÁTOR, ALE DATA SE MUSÍ VYTÁHNOUT Z DATABÁZE

# DATA Z DATABÁZE SE NÁSLEDNĚ MUSÍ ALE ULOŽIT STEJNĚ JAKO TY Z GENERÁTORU, ABY FUNGOVALY STEJNĚ V OVM FUNCKI

    find_mob = Mobs_dungeons.objects.filter(mob_id=mob_id).first()
    mob = {
        'name': find_mob.name,
        'mob_id': mob_id,
        'dificulty_koeficient': find_mob.dificulty_koeficient,
        'lvl': find_mob.lvl,
        'hp': find_mob.hp,
        'str': find_mob.str,
        'dex': find_mob.dex,
        'int': find_mob.int,
        'vit': find_mob.vit,
        'luck': find_mob.luck,
        'dmg_atr': find_mob.dmg_atr,
        'magic_resist': find_mob.magic_resist,
        'light_resist': find_mob.light_resist,
        'heavy_resist': find_mob.heavy_resist,
        'otrava_resist': find_mob.otrava_resist,
        'bezvedomi_resist': find_mob.bezvedomi_resist,
        'poskozeni_schopnosti': find_mob.poskozeni_schopnosti,
        'poskozeni_utokem': find_mob.poskozeni_utokem,
        'sance_na_otravu': find_mob.sance_na_otravu,
        'sance_na_bezvedomi': find_mob.sance_na_bezvedomi,
        'sance_na_kriticky_utok': find_mob.sance_na_kriticky_utok,
        'kriticke_poskozeni': find_mob.kriticke_poskozeni,
        'armor': find_mob.armor,
        'min_dmg': find_mob.min_dmg,
        'max_dmg': find_mob.max_dmg
    }

    fight_uuid = pvm_fight_funkce(request, mob)
    fight_log_entries = FightLogEntry.objects.filter(fight_id=fight_uuid).order_by('timestamp')
    if fight_log_entries:
        winner_name = Fight.objects.filter(fight_id=fight_uuid).first().winner

    if winner_name == user.username:
        loot = loot_gen(request, mob)
    else:
        loot = None

    Dungeon_progress.objects.filter(hrac=user).create(
        hrac=user,
        id_of_mobs_cleared=mob_id,
        get_xp=loot['xp'] if loot else 0,
        get_gold=loot['gold'] if loot else 0
    )

    # + IMPORTOVAT INFORMACE O MOBCE A O HRÁČI, V SOUBOJI JE ČISTĚ SOUBOJ
    return render(request, 'pvmapp/dungeon_mob_arena.html', {
        'fight_uuid': fight_uuid, 
        'winner_name': winner_name,
        'fight_log_entries': fight_log_entries,
        'loot': loot,
        'mob': mob
        })

@login_required
def random_mob_fight(request):

    user = request.user
    mob = mob_gen(request)
    fight_uuid = pvm_fight_funkce(request, mob)
    fight_log_entries = FightLogEntry.objects.filter(fight_id=fight_uuid).order_by('timestamp')
    if fight_log_entries:
        winner_name = Fight.objects.filter(fight_id=fight_uuid).first().winner

    if winner_name == user.username:
        loot = loot_gen(request, mob)
    else:
        loot = None

    # + IMPORTOVAT INFORMACE O MOBCE A O HRÁČI, V SOUBOJI JE ČISTĚ SOUBOJ

    return render(request, 'pvmapp/random_mob_arena.html', {
        'fight_uuid': fight_uuid, 
        'winner_name': winner_name,
        'fight_log_entries': fight_log_entries,
        'loot': loot
        })

@login_required
def pvm_home(request):
    user = request.user

    context = {
        'user': user,

    }
    return render(request, 'pvmapp/pvm_home.html', context)

@login_required
def dungeon_map_chosen(request):
    user = request.user

    if request.method == 'POST':
        chosen_map = request.POST.get('locations')
        chosen_map = int(chosen_map) if chosen_map else None
        print(chosen_map)
        if chosen_map == 1:
            relevant_mobs = Mobs_dungeons.objects.filter(dungeon=chosen_map)
            return render(request, 'pvmapp/base_camp.html', {
                'relevant_mobs': relevant_mobs
            })


    else:
        context = {
            'user': user,

        }
        return render(request, 'pvmapp/dungeon_map.html', context)






@login_required
def dungeon_map_all(request):
    user = request.user

    context = {
        'user': user,

    }
    return render(request, 'pvmapp/dungeon_map.html', context)

