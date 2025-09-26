
from django.shortcuts import render
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from hracapp. models import FightLogEntry, Fight
from .mob_generator import mob_gen
from .pvm_fight import pvm_fight_funkce
from .loot_gen import loot_gen


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





