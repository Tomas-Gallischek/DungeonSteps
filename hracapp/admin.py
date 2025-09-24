from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Economy_Log, FightLogEntry, Playerinfo, XP_LVL, Economy, Atributs, INV, EQP, Character_bonus, ShopOffer, XP_Log


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
        ShopOfferInline,
        INVInline,
        EQPInline,
        XP_LogInline,
        EconomyLogInline,
    ]

# ==== SAMOSTATNÁ REGISTRACE MODELU CHARACTER_BONUS ====

@admin.register(Character_bonus)
class CharacterBonusAdmin(admin.ModelAdmin):
    list_display = ('hrac', 'hp_flat_it_bonus', 'pvm_resist_procent_it_bonus')
    search_fields = ('hrac__username',)
    readonly_fields = [field.name for field in Character_bonus._meta.fields]

class FightLogEntryAdmin(admin.ModelAdmin):
    model = FightLogEntry
    extra = 0
    can_delete = True
    readonly_fields = ('fight_id', 'user', 'mob', 'round_number', 'description', 'event_type', 'timestamp', 'player_hp_before', 'player_hp_after', 'mob_hp_before', 'mob_hp_after')
    verbose_name_plural = 'Záznamy soubojů'

admin.site.register(FightLogEntry, FightLogEntryAdmin)