from hmac import new
import json
from django.contrib.auth import logout
from django.shortcuts import redirect, render
from django.urls import reverse
from django.shortcuts import render, redirect
from .off_deff import fight_def, fight_off, iniciace
from .rasy_povolani import povolani_bonus, rasa_bonus
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from django.http import JsonResponse
from .utils import calculate_xp_and_level, calculate_gold, atributy_hodnota, atributy_cena
from . models import EQP, INV


@login_required
def profile(request):
    # Inicializace RASY A POVOLÁNÍ
    povolani_bonus(request)
    rasa_bonus(request)

# Volání funkce pro atributy
    hp_bonus_vitality, suma_atributy, base_atributy, plus_atributy, plus_strength, plus_dexterity, plus_intelligence, plus_charisma, plus_vitality, plus_luck = atributy_hodnota(request)

# Volání funkce pro cenu atributů
    atributy_cost = atributy_cena(request)

# Volání funkce pro LVL
    XP_aktual, lvl_aktual, lvl_next, XP_potrebne_next  = calculate_xp_and_level(request)

# Volání funkce pro Gold
    collected_gold, gold_growth_coefficient, gold_limit, gold_per_hour = calculate_gold(request)

# Ofenzivní a defenzivní statistiky
    crit_chance, center_dmg, min_dmg, max_dmg, weapon_typ = fight_off(request)
    heavy_res, magic_res, light_res, dodge_chance = fight_def(request)
    inicial_number = iniciace(request)

# VOLÁNÍ FUNKCE PRO VÝPIS INVENTÁŘE
    inventory_items = inventory(request)

# VOLÁNÍ FUNKCE PRO VÝPIS NASAZENÝCH ITEMŮ
    equipment_items = equipment(request)

    # Korky hráče
    user_steps = request.user.steps if request.user.steps is not None else 0
    # POST formuláře
    if request.method == 'POST':
        action = request.POST.get('action')
        if action == 'collect_gold':
            user = request.user
            user_gold = user.economy
            user_gold.gold += collected_gold
            user_gold.last_gold_collection = timezone.now()
            user_gold.save()
            messages.success(request, 'Goldy úspěšně sebrány!')
            return redirect('profile-url')

    # Kontext pro render
    context = {
    # XP A LVL
        'steps': user_steps,
        'XP_aktual': XP_aktual,
        'lvl_aktual': lvl_aktual,
        'lvl_next': lvl_next,
        'XP_potrebne_next': XP_potrebne_next,
    # GOLDY
        'gold_own': request.user.economy.gold,
        'collected_gold': collected_gold,
        'gold_growth_coefficient': gold_growth_coefficient,
        'gold_limit': gold_limit,
        'gold_per_hour': gold_per_hour,
    # ATRIBUTY - BASE
        'base_hp': base_atributy["base_hp"],
        'base_strength': base_atributy["base_strength"],
        'base_dexterity': base_atributy["base_dexterity"],
        'base_intelligence': base_atributy["base_intelligence"],
        'base_charisma': base_atributy["base_charisma"],
        'base_vitality': base_atributy["base_vitality"],
        'base_luck': base_atributy["base_luck"],
    # ATRIBUTY - PLUS
        'plus_hp': plus_atributy["plus_hp"],
        'plus_strength': plus_atributy["plus_strength"],
        'plus_dexterity': plus_atributy["plus_dexterity"],
        'plus_intelligence': plus_atributy["plus_intelligence"],
        'plus_charisma': plus_atributy["plus_charisma"],
        'plus_vitality': plus_atributy["plus_vitality"],
        'plus_luck': plus_atributy["plus_luck"],
    # ATRIBUTY - SUMA
        'suma_hp': suma_atributy["suma_hp"],
        'suma_strength': suma_atributy["suma_strength"],
        'suma_dexterity': suma_atributy["suma_dexterity"],
        'suma_intelligence': suma_atributy["suma_intelligence"],
        'suma_charisma': suma_atributy["suma_charisma"],
        'suma_vitality': suma_atributy["suma_vitality"],
        'suma_luck': suma_atributy["suma_luck"],
        'hp_bonus_vitality': hp_bonus_vitality,
    # ATRIBUTY - CENA
        'strength_cost': atributy_cost["strength_cost"],
        'dexterity_cost': atributy_cost["dexterity_cost"],
        'intelligence_cost': atributy_cost["intelligence_cost"],
        'charisma_cost': atributy_cost["charisma_cost"],
        'vitality_cost': atributy_cost["vitality_cost"],
        'luck_cost': atributy_cost["luck_cost"],
    # OFF 
        'crit_chance': crit_chance,
        'center_dmg': center_dmg,
        'weapon_typ': weapon_typ,
    # DEF
        'heavy_res': heavy_res,
        'magic_res': magic_res,
        'light_res': light_res,
        'dodge_chance': dodge_chance,
    # INVENTÁŘ
        'inventory_items': inventory_items,
    # EQUIP
        'equipment_items': equipment_items,
    # OSTATNÍ
        'inicial_number': inicial_number,
    }
       

    return render(request, 'hracapp/profile.html', context)



def custom_logout(request):
    if request.method == 'POST':
        logout(request)
        return render(request, 'hracapp/logout.html')
    return redirect('profile-url')

def update_steps(request):
    if request.method == 'POST':
        new_steps = request.POST.get('steps')
        if new_steps is not None:
            request.user.steps = new_steps
            request.user.save()
            messages.success(request, 'Kroky byly úspěšně aktualizovány.')
        else:
            messages.error(request, 'Nezadali jste platnou hodnotu kroků.')
    return render(request, 'hracapp/steps_input.html')

def update_attribute(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            attribute_to_update = data.get('attribute')

            # Zkontroluje, zda je atribut platný
            valid_attributes = ['strength', 'dexterity', 'intelligence', 'charisma', 'vitality', 'luck']
            if attribute_to_update in valid_attributes:

                user = request.user
                user_gold = user.economy
                user_atributs = user.atributy

                # Získáme aktuální ceny
                current_prices = atributy_cena(request)
                atribut_bill = current_prices.get(f'{attribute_to_update}_cost')

                # Kontrola dostatku goldů
                if user_gold.gold < atribut_bill:
                    return JsonResponse({'success': False, 'error': 'Nedostatek zlata.'}, status=403)

                # Odečtení ceny atributu z uživatelských goldů a uložení
                user_gold.gold -= atribut_bill

                # Aktualizace správného atributu (plus) a uložení
                current_plus_value = getattr(user_atributs, f'{attribute_to_update}_plus')
                setattr(user_atributs, f'{attribute_to_update}_plus', current_plus_value + 1)


                user_atributs.save()
                user_gold.save()
                user.save()

                # Speciální případ pro vitalitu, kde se aktualizují HP
                if attribute_to_update == 'vitality':
                    user_atributs.HP = atributy_hodnota(request)[0]['suma_hp']

                # Vypočítá nové ceny a hodnoty atributů po aktualizaci
                hp_bonus_vitality, suma_atributy, base_atributy, plus_atributy, plus_strength, plus_dexterity, plus_intelligence, plus_charisma, plus_vitality, plus_luck = atributy_hodnota(request)

                new_value = suma_atributy.get(f'suma_{attribute_to_update}')

                atributy_cost = atributy_cena(request)
                new_price = atributy_cost.get(f'{attribute_to_update}_cost')

                # Sestavení a vrácení odpovědi
                response_data = {
                    'success': True,
                    'new_value': new_value,
                    'new_prices': new_price,
                    'new_golds': user_gold.gold,
                    'new_hp': suma_atributy['suma_hp'] if attribute_to_update == 'vitality' else user_atributs.HP,
                }
                return JsonResponse(response_data)
            else:
                return JsonResponse({'success': False, 'error': 'Neplatný atribut.'}, status=400)
        except json.JSONDecodeError:
            return JsonResponse({'success': False, 'error': 'Neplatná JSON data.'}, status=400)
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)}, status=500)

    return JsonResponse({'success': False, 'error': 'Neplatná metoda požadavku.'}, status=405)

def gold_per_second(request):
    print("Volání gold_per_second")
    lvl_aktual = calculate_xp_and_level(request)[1]
    golds_info = calculate_gold(request.user, lvl_aktual)
    collected_gold = golds_info[0]
    aktualizovana_hodnota = collected_gold

    # Vrácení dat jako JSON
    data = {
        'hodnota': aktualizovana_hodnota,
    }
    return JsonResponse(data)

def inventory(request):
    user = request.user
    inventory_items = INV.objects.filter(hrac=user)

    return inventory_items

def equipment(request):
    user = request.user
    equipment_items = EQP.objects.filter(hrac=user)
    return equipment_items

def equip_item(request, item_id):
    user = request.user
    inventary = INV.objects.filter(hrac=user)
    item = inventary.get(item_id=item_id)
    item_to_equip = EQP (
        hrac=user,
        item_id=item.item_id,
        item_type=item.item_type,
        item_name=item.item_name,
        item_price=item.item_price,
        item_description=item.item_description,
        item_level_stop=item.item_level_stop,
        item_level_required=item.item_level_required,
        item_base_damage=item.item_base_damage,
        item_weapon_type=item.item_weapon_type,
        item_max_damage=item.item_max_damage,
        item_min_damage=item.item_min_damage,
        item_slots=item.item_slots
    )
    item_to_equip.save()

    INV.objects.filter(hrac=user, item_id=item_id).delete()

    print(f"Item: {item.item_name} byl úspěšně nasazen.")

    return redirect(reverse('profile-url'))

def dequip_item(request, item_id):
    user = request.user
    equipment = EQP.objects.filter(hrac=user)
    item = equipment.filter(item_id=item_id).first()
    item_to_de_equip = INV (
        hrac=user,
        item_id=item.item_id,
        item_type=item.item_type,
        item_name=item.item_name,
        item_price=item.item_price,
        item_description=item.item_description,
        item_level_stop=item.item_level_stop,
        item_level_required=item.item_level_required,
        item_base_damage=item.item_base_damage,
        item_weapon_type=item.item_weapon_type,
        item_max_damage=item.item_max_damage,
        item_min_damage=item.item_min_damage,
        item_slots=item.item_slots
    )
    item_to_de_equip.save()

    EQP.objects.filter(hrac=user, item_id=item_id).delete()
    print(f"Item: {item.item_name} byl úspěšně sundán.")
    return redirect(reverse('profile-url'))