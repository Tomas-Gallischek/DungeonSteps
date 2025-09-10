from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Economy_Log, Playerinfo, XP_LVL, Economy, Atributs, INV, EQP, Character_bonus, ShopOffer, XP_Log


# ==== INLINES ====

class XPLVLInline(admin.StackedInline):
    model = XP_LVL
    can_delete = False
    verbose_name_plural = 'XP a Level'


class EconomyInline(admin.StackedInline):
    model = Economy
    can_delete = False
    verbose_name_plural = 'Ekonomika'


class AtributsInline(admin.StackedInline):
    model = Atributs
    can_delete = False
    verbose_name_plural = 'Atributy'


class CharacterBonusInline(admin.StackedInline):
    model = Character_bonus
    can_delete = False
    verbose_name_plural = 'Bonusy postavy'

class ShopOfferInline(admin.TabularInline):
    model = ShopOffer
    extra = 0
    verbose_name_plural = 'Nabídky obchodu'


class INVInline(admin.TabularInline):
    model = INV
    extra = 0
    verbose_name_plural = 'Inventář'


class EQPInline(admin.TabularInline):
    model = EQP
    extra = 0
    verbose_name_plural = 'Vybavení'

class XP_LogInline(admin.TabularInline):
    model = XP_Log
    extra = 0
    can_delete = False
    readonly_fields = ('timestamp',)
    verbose_name_plural = 'Záznamy XP'

class EconomyLogInline(admin.TabularInline):
    model = Economy_Log
    extra = 0
    can_delete = False
    readonly_fields = ('timestamp',)
    verbose_name_plural = 'Záznamy ekonomiky'

# ==== PLAYERINFO ADMIN ====

@admin.register(Playerinfo)
class PlayerinfoAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + (
        ('Základní informace', {
            'fields': ('name', 'surname', 'gender', 'rasa', 'povolani')
        }),
        # POZOR: vynechali jsme last_login a date_joined, už je má UserAdmin
    )

    add_fieldsets = UserAdmin.add_fieldsets + (
        (None, {'fields': ('name', 'surname', 'gender', 'rasa', 'povolani')}),
    )

    list_display = UserAdmin.list_display + (
        'name', 'surname', 'gender', 'rasa', 'povolani'
    )

    inlines = [
        XPLVLInline,
        EconomyInline,
        AtributsInline,
        CharacterBonusInline,
        ShopOfferInline,
        INVInline,
        EQPInline,
        XP_LogInline,
        EconomyLogInline,
    ]

