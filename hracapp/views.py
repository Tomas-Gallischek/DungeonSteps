from django.contrib.auth import logout
from django.shortcuts import redirect, render
from django.urls import reverse
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .off_deff import off_stats, def_stats
from . models import EQP, INV, XP_LVL, Economy, Atributs


@login_required
def profile(request):

    inventory_items = inventory(request)
    equipment_items = equipment(request)

    context = {
    # XP A LVL
        'XP_aktual': XP_LVL.objects.get(hrac=request.user).xp,
        'lvl_aktual': XP_LVL.objects.get(hrac=request.user).lvl,
        'lvl_next': XP_LVL.objects.get(hrac=request.user).lvl + 1,
        'XP_potrebne_next': XP_LVL.objects.get(hrac=request.user).xp_to_next_lvl,
        'xp_nasetrene': XP_LVL.objects.get(hrac=request.user).xp_nasetreno,
    # GOLDY
        'gold_own': Economy.objects.get(hrac=request.user).gold,
        'dungeon_token_own': Economy.objects.get(hrac=request.user).dungeon_token,
    # ATRIBUTY - BASE
        'base_hp': Atributs.objects.get(hrac=request.user).hp_base,
        'base_strength': Atributs.objects.get(hrac=request.user).strength_base,
        'base_dexterity': Atributs.objects.get(hrac=request.user).dexterity_base,
        'base_intelligence': Atributs.objects.get(hrac=request.user).intelligence_base,
        'base_charisma': Atributs.objects.get(hrac=request.user).charisma_base,
        'base_vitality': Atributs.objects.get(hrac=request.user).vitality_base,
        'base_luck': Atributs.objects.get(hrac=request.user).luck_base,
    # ATRIBUTY - PLUS
        'plus_hp': Atributs.objects.get(hrac=request.user).hp_vit,
        'plus_strength': Atributs.objects.get(hrac=request.user).strength_plus,
        'plus_dexterity': Atributs.objects.get(hrac=request.user).dexterity_plus,
        'plus_intelligence': Atributs.objects.get(hrac=request.user).intelligence_plus,
        'plus_charisma': Atributs.objects.get(hrac=request.user).charisma_plus,
        'plus_vitality': Atributs.objects.get(hrac=request.user).vitality_plus,
        'plus_luck': Atributs.objects.get(hrac=request.user).luck_plus,
    # ATRIBUTY - SUMA
        'suma_hp': Atributs.objects.get(hrac=request.user).suma_hp,
        'suma_strength': Atributs.objects.get(hrac=request.user).suma_strength,
        'suma_dexterity': Atributs.objects.get(hrac=request.user).suma_dexterity,
        'suma_intelligence': Atributs.objects.get(hrac=request.user).suma_intelligence,
        'suma_charisma': Atributs.objects.get(hrac=request.user).suma_charisma,
        'suma_vitality': Atributs.objects.get(hrac=request.user).suma_vitality,
        'suma_luck': Atributs.objects.get(hrac=request.user).suma_luck,
    # ATRIBUTY - CENA
        'strength_cost': Atributs.objects.get(hrac=request.user).strength_cena,
        'dexterity_cost': Atributs.objects.get(hrac=request.user).dexterity_cena,
        'intelligence_cost': Atributs.objects.get(hrac=request.user).intelligence_cena,
        'charisma_cost': Atributs.objects.get(hrac=request.user).charisma_cena,
        'vitality_cost': Atributs.objects.get(hrac=request.user).vitality_cena,
        'luck_cost': Atributs.objects.get(hrac=request.user).luck_cena,

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
    inventary = INV.objects.filter(hrac=user)
    item = inventary.get(item_id=item_id)

    EQP.objects.create(
        hrac=item.hrac,
        item_id=item.item_id,
        name=item.name,
        img_init=item.img_init,
        description=item.description,
        level_required=item.level_required,
        level_stop=item.level_stop,
        item_type=item.item_type,
        item_category=item.item_category,
        slots=item.slots,
        slot_1_bonus=item.slot_1_bonus,
        slot_1_value=item.slot_1_value,
        slot_2_bonus=item.slot_2_bonus,
        slot_2_value=item.slot_2_value,
        slot_3_bonus=item.slot_3_bonus,
        slot_3_value=item.slot_3_value,
        slot_4_bonus=item.slot_4_bonus,
        slot_4_value=item.slot_4_value,
        price=item.price,
        min_dmg=item.min_dmg,
        max_dmg=item.max_dmg,
        prum_dmg=item.prum_dmg,
        armor=item.armor,
        str_bonus=item.str_bonus,
        dex_bonus=item.dex_bonus,
        int_bonus=item.int_bonus,
        vit_bonus=item.vit_bonus,
        luk_bonus=item.luk_bonus,
    )

    INV.objects.filter(hrac=user, item_id=item_id).delete()

    print(f"Item: {item.name} byl úspěšně nasazen.")

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
        slot_1_bonus=item.slot_1_bonus,
        slot_1_value=item.slot_1_value,
        slot_2_bonus=item.slot_2_bonus,
        slot_2_value=item.slot_2_value,
        slot_3_bonus=item.slot_3_bonus,
        slot_3_value=item.slot_3_value,
        slot_4_bonus=item.slot_4_bonus,
        slot_4_value=item.slot_4_value,
        price=item.price,
        min_dmg=item.min_dmg,
        max_dmg=item.max_dmg,
        prum_dmg=item.prum_dmg,
        armor=item.armor,
        str_bonus=item.str_bonus,
        dex_bonus=item.dex_bonus,
        int_bonus=item.int_bonus,
        vit_bonus=item.vit_bonus,
        luk_bonus=item.luk_bonus,
    )

    EQP.objects.filter(hrac=user, item_id=item_id).delete()
    print(f"Item: {item.name} byl úspěšně sundán.")
    return redirect(reverse('profile-url'))