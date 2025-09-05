from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Playerinfo, XP_LVL, Economy, Atributs, INV, EQP, Character_bonus, ShopOffer, XP_Log

# Inlines pro související modely
class XPLVLInline(admin.TabularInline):
    model = XP_LVL
    can_delete = False
    verbose_name_plural = 'XP a Level'

class EconomyInline(admin.TabularInline):
    model = Economy
    can_delete = False
    verbose_name_plural = 'Ekonomika'

class AtributsInline(admin.TabularInline):
    model = Atributs
    can_delete = False
    verbose_name_plural = 'Atributy'

class INVInline(admin.TabularInline):
    model = INV
    can_delete = False
    verbose_name_plural = 'Inventář'

class EQPInline(admin.TabularInline):
    model = EQP
    can_delete = False
    verbose_name_plural = 'Vybavení'

class CharacterBonusInline(admin.TabularInline):
    model = Character_bonus
    can_delete = False
    verbose_name_plural = 'Bonusy postavy'

class ShopOfferInline(admin.TabularInline):
    model = ShopOffer
    can_delete = False
    verbose_name_plural = 'Nabídky obchodu'

class XP_LogInline(admin.TabularInline):
    model = XP_Log
    extra = 1
    readonly_fields = ('timestamp',)

# Vlastní Admin třída pro Playerinfo s inlines.
# Dekorátor @admin.register(Playerinfo) zajistí správnou registraci.
@admin.register(Playerinfo)
class PlayerinfoAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('name', 'surname', 'gender', 'rasa', 'povolani')}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        (None, {'fields': ('name', 'surname', 'gender', 'rasa', 'povolani')}),
    )
    list_display = UserAdmin.list_display + ('name', 'surname', 'gender', 'rasa', 'povolani')
    inlines = [XPLVLInline, EconomyInline, AtributsInline, CharacterBonusInline, ShopOfferInline, XP_LogInline]


# Registrace modelů INV a EQP jako samostatných entit v admin rozhraní
admin.site.register(INV)
admin.site.register(EQP)