from encodings.punycode import selective_len
from operator import eq
from urllib import request
from django.contrib.auth import logout
from django.shortcuts import redirect, render
from django.urls import reverse
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .off_deff import off_stats, def_stats
from . models import EQP, INV, XP_LVL, Character_bonus, Economy, Atributs, ShopOffer



@login_required
def profile(request):

    #INV.objects.all().delete()
    #EQP.objects.all().delete()
    #ShopOffer.objects.all().delete()
    user = request.user
    inventory_items = inventory(request)
    equipment_items = equipment(request)
    xp_lvl_data = XP_LVL.objects.get(hrac=user)
    economy_data = Economy.objects.get(hrac=user)
    atributs_data = Atributs.objects.get(hrac=user)


    context = {
    # XP A LVL
        'XP_aktual': xp_lvl_data.xp,
        'lvl_aktual': xp_lvl_data.lvl,
        'lvl_next': xp_lvl_data.lvl + 1,
        'XP_potrebne_next': xp_lvl_data.xp_to_next_lvl,
        'xp_nasetrene': xp_lvl_data.xp_nasetreno,
    # GOLDY
        'gold_own': economy_data.gold,
        'dungeon_token_own': economy_data.dungeon_token,
    # ATRIBUTY - BASE
        'base_hp': atributs_data.hp_base,
        'base_strength': atributs_data.strength_base,
        'base_dexterity': atributs_data.dexterity_base,
        'base_intelligence': atributs_data.intelligence_base,
        'base_charisma': atributs_data.charisma_base,
        'base_vitality': atributs_data.vitality_base,
        'base_luck': atributs_data.luck_base,
    # ATRIBUTY - PLUS
        'plus_hp': atributs_data.hp_vit,
        'plus_strength': atributs_data.strength_plus,
        'plus_dexterity': atributs_data.dexterity_plus,
        'plus_intelligence': atributs_data.intelligence_plus,
        'plus_charisma': atributs_data.charisma_plus,
        'plus_vitality': atributs_data.vitality_plus,
        'plus_luck': atributs_data.luck_plus,
    # ATRIBUTY - SUMA
        'suma_hp': atributs_data.suma_hp,
        'suma_strength': atributs_data.suma_strength,
        'suma_dexterity': atributs_data.suma_dexterity,
        'suma_intelligence': atributs_data.suma_intelligence,
        'suma_charisma': atributs_data.suma_charisma,
        'suma_vitality': atributs_data.suma_vitality,
        'suma_luck': atributs_data.suma_luck,
    # ATRIBUTY - CENA
        'strength_cost': atributs_data.strength_cena,
        'dexterity_cost': atributs_data.dexterity_cena,
        'intelligence_cost': atributs_data.intelligence_cena,
        'charisma_cost': atributs_data.charisma_cena,
        'vitality_cost': atributs_data.vitality_cena,
        'luck_cost': atributs_data.luck_cena,

    # INVENTÁŘ
        'inventory_items': inventory_items,
    # EQUIP
        'equipment_items': equipment_items,
    # OSTATNÍ
        'rasa': request.user.rasa,
        'povolani': request.user.povolani,
        'hrac': request.user,
    }
       

    return render(request, 'hracapp/profile.html', context)


def custom_logout(request):
    if request.method == 'POST':
        logout(request)
        return render(request, 'hracapp/logout.html')
    return redirect('profile-url')

def inventory(request):
    user = request.user
    inventory_items = INV.objects.filter(hrac=user)

    return inventory_items

def equipment(request):
    user = request.user
    equipment_items = EQP.objects.filter(hrac=user)
    return equipment_items

def equip_item(request, item_id):
    print(f"Equipping item with ID: {item_id}")
    user = request.user
    
    # 1. Najdi předmět v inventáři, který chceme nasadit.
    try:
        item = INV.objects.get(hrac=user, item_id=item_id)
    except INV.DoesNotExist:
        print(f"Chyba: Předmět s ID {item_id} nebyl nalezen v inventáři hráče.")
        return redirect(reverse('profile-url'))

    # 2. Zkontroluj, jestli má hráč už nasazený předmět stejné kategorie a pokud ano, sundej ho.
    try:
        existing_equipped_item = EQP.objects.get(hrac=user, item_category=item.item_category)
        print(f"Existující předmět: {existing_equipped_item.name} ve stejné kategorii nalezen.")
        dequip_item(request, existing_equipped_item.item_id)
    except EQP.DoesNotExist:
        # Žádný předmět není nasazen, není co sundávat.
        print(f"Žádný předmět kategorie '{item.item_category}' není nasazen. Pokračuji v nasazování.")
    
    # 3. Nyní nasadíme nový předmět (tento blok se provede vždy).
    EQP.objects.create(
        hrac=user,
        item_id=item.item_id,
        name=item.name,
        img_init=item.img_init,
        description=item.description,
        level_required=item.level_required,
        level_stop=item.level_stop,
        item_type=item.item_type,
        item_category=item.item_category,
        slots=item.slots,
        price=item.price,
        sell_price=item.sell_price,
        min_dmg=item.min_dmg,
        max_dmg=item.max_dmg,
        prum_dmg=item.prum_dmg,
        armor=item.armor,
        str_bonus=item.str_bonus,
        dex_bonus=item.dex_bonus,
        int_bonus=item.int_bonus,
        vit_bonus=item.vit_bonus,
        luk_bonus=item.luk_bonus,
        kriticke_poskozeni_procenta_it_bonus=item.kriticke_poskozeni_procenta_it_bonus,
        sance_na_bezvedomi_procenta_it_bonus=item.sance_na_bezvedomi_procenta_it_bonus,
        sance_na_otravu_procenta_it_bonus=item.sance_na_otravu_procenta_it_bonus,
        poskozeni_utokem_procenta_it_bonus=item.poskozeni_utokem_procenta_it_bonus,
        poskozeni_schopnosti_procenta_it_bonus=item.poskozeni_schopnosti_procenta_it_bonus,
        pvp_poskozeni_procenta_it_bonus=item.pvp_poskozeni_procenta_it_bonus,
        pvm_poskozeni_procenta_it_bonus=item.pvm_poskozeni_procenta_it_bonus,
        str_flat_it_bonus=item.str_flat_it_bonus,
        dex_flat_it_bonus=item.dex_flat_it_bonus,
        int_flat_it_bonus=item.int_flat_it_bonus,
        vit_flat_it_bonus=item.vit_flat_it_bonus,
        luck_flat_it_bonus=item.luck_flat_it_bonus,
        bezvedomi_resist_procenta_it_bonus=item.bezvedomi_resist_procenta_it_bonus,
        otrava_resist_procenta_it_bonus=item.otrava_resist_procenta_it_bonus,
        light_resist_procenta_it_bonus=item.light_resist_procenta_it_bonus,
        heavy_resist_procenta_it_bonus=item.heavy_resist_procenta_it_bonus,
        magic_resist_procenta_it_bonus=item.magic_resist_procenta_it_bonus,
        pvp_resist_procenta_it_bonus=item.pvp_resist_procenta_it_bonus,
        pvm_resist_procenta_it_bonus=item.pvm_resist_procenta_it_bonus,
        hp_flat_it_bonus=item.hp_flat_it_bonus
    )
    # Odstranění předmětu z inventáře.
    INV.objects.filter(hrac=user, item_id=item_id).delete()

    print(f"Item: {item.name} byl úspěšně nasazen.")

    # 4. Aktualizace bonusů a přesměrování.
    character_bonus_instance = Character_bonus.objects.get(hrac=user)
    character_bonus_instance.save()

    return redirect(reverse('profile-url'))

def dequip_item(request, item_id):
    user = request.user
    equipment = EQP.objects.filter(hrac=user)
    item = equipment.get(item_id=item_id)

    INV.objects.create(
            hrac=user,
            item_id=item.item_id,
            name=item.name,
            img_init=item.img_init,
            description=item.description,
            level_required=item.level_required,
            level_stop=item.level_stop,
            item_type=item.item_type,
            item_category=item.item_category,
            slots=item.slots,
            price=item.price,
            sell_price=item.sell_price,
            min_dmg=item.min_dmg,
            max_dmg=item.max_dmg,
            prum_dmg=item.prum_dmg,
            armor=item.armor,
            str_bonus=item.str_bonus,
            dex_bonus=item.dex_bonus,
            int_bonus=item.int_bonus,
            vit_bonus=item.vit_bonus,
            luk_bonus=item.luk_bonus,
            kriticke_poskozeni_procenta_it_bonus=item.kriticke_poskozeni_procenta_it_bonus,
            sance_na_bezvedomi_procenta_it_bonus=item.sance_na_bezvedomi_procenta_it_bonus,
            sance_na_otravu_procenta_it_bonus=item.sance_na_otravu_procenta_it_bonus,
            poskozeni_utokem_procenta_it_bonus=item.poskozeni_utokem_procenta_it_bonus,
            poskozeni_schopnosti_procenta_it_bonus=item.poskozeni_schopnosti_procenta_it_bonus,
            pvp_poskozeni_procenta_it_bonus=item.pvp_poskozeni_procenta_it_bonus,
            pvm_poskozeni_procenta_it_bonus=item.pvm_poskozeni_procenta_it_bonus,
            str_flat_it_bonus=item.str_flat_it_bonus,
            dex_flat_it_bonus=item.dex_flat_it_bonus,
            int_flat_it_bonus=item.int_flat_it_bonus,
            vit_flat_it_bonus=item.vit_flat_it_bonus,
            luck_flat_it_bonus=item.luck_flat_it_bonus,
            bezvedomi_resist_procenta_it_bonus=item.bezvedomi_resist_procenta_it_bonus,
            otrava_resist_procenta_it_bonus=item.otrava_resist_procenta_it_bonus,
            light_resist_procenta_it_bonus=item.light_resist_procenta_it_bonus,
            heavy_resist_procenta_it_bonus=item.heavy_resist_procenta_it_bonus,
            magic_resist_procenta_it_bonus=item.magic_resist_procenta_it_bonus,
            pvp_resist_procenta_it_bonus=item.pvp_resist_procenta_it_bonus,
            pvm_resist_procenta_it_bonus=item.pvm_resist_procenta_it_bonus,
            hp_flat_it_bonus=item.hp_flat_it_bonus
    )

    EQP.objects.filter(hrac=user, item_id=item_id).delete()
    print(f"Item: {item.name} byl úspěšně sundán.")

    character_bonus_instance, created = Character_bonus.objects.get_or_create(hrac=request.user)
    character_bonus_instance = Character_bonus.objects.get(hrac=user)
    character_bonus_instance.save()

    return redirect(reverse('profile-url'))