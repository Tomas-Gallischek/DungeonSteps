from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone

# HLAVNÍ DATABÁZE HRÁČE:
class Playerinfo(AbstractUser):
    ITEM_TYPE_CHOICES = [
    ('weapon', 'Zbraň'),
    ('armor', 'Brnění'),
]
    GENDER_CHOICES = (
    ('male', 'Muž'),
    ('female', 'Žena'),
    ('other', 'Jiné'),
)
    RASA_CHOICES = (
        ('Choice:', 'Vyber:'),
        ('human', 'Člověk'),
        ('elf', 'Elf'),
        ('dwarf', 'Trpaslík'),
        ('urgal', 'Urgal'),
        ('gnóm', 'Gnóm'),
        ('shadow', 'Stín'),
    )
    POVOLANI_CHOICES = (
        ('choice:', 'Vyber:'),
        ('ranger', 'Hraničář'),
        ('monk', 'Mnich'),
        ('warrior', 'Válečník'),
        ('paladin', 'Paladin'),
        ('mage', 'Mág'),
        ('rogue', 'Roguna'),
        ('necromancer', 'Nekromant'),
        ('berserker', 'Ničitel'),
        ('druid', 'Druid')
    )
    ATRIBUTS_CHOICES = (
        ('strength', 'Síla'),
        ('dexterity', 'Obratnost'),
        ('intelligence', 'Inteligence'),
        ('charisma', 'Charisma'),
        ('luck', 'Štěstí'),
        ('vitality', 'Vitalita')
    )

    username = models.CharField(max_length=150, unique=True)
    name = models.CharField(max_length=100, blank=True, null=True)
    surname = models.CharField(max_length=100, blank=True, null=True)
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES, blank=True, null=True)
    steps = models.IntegerField(("Počet kroků"), blank=True, null=True)
    rasa = models.CharField(max_length=20, choices=RASA_CHOICES, blank=True, null=True)
    povolani = models.CharField(max_length=20, choices=POVOLANI_CHOICES, blank=True, null=True)

def __str__(self):
    return self.username

# VŠECHNY VNOŘENÉ DATABÁZE
class XP_LVL(models.Model):
    hrac = models.OneToOneField(Playerinfo, on_delete=models.CASCADE, related_name='xp_lvl', blank=True)
    lvl = models.IntegerField(("Úroveň"), default=1, blank=True, null=True)
    xp = models.IntegerField(("Zkušenosti"), default=0, blank=True, null=True)


class Economy(models.Model):
    hrac = models.OneToOneField(Playerinfo, on_delete=models.CASCADE, related_name='economy', blank=True)
    gold = models.IntegerField(("Počet GOLDŮ"), default=1)
    rohlik = models.IntegerField(("Počet ROHLÍKŮ"), default=1)
    gold_growth_coefficient = models.FloatField(("Koeficient růstu GOLDŮ"), default=1.0)
    last_gold_collection = models.DateTimeField(blank=True, null=True, default=timezone.now)
class Atributs(models.Model):
    hrac = models.OneToOneField(Playerinfo, on_delete=models.CASCADE, related_name='atributy', blank=True)
    HP = models.IntegerField(("Počet životů"), default=10, blank=True, null=True)
    hp_bonus = models.FloatField(("Bonus k životům"), default=1, blank=True, null=True)

    suma_strength = models.IntegerField(("Síla"), default=1, blank=True, null=True)
    strength_base = models.IntegerField(("Základní síla"), default=1, blank=True, null=True)
    strength_plus = models.IntegerField(("plus k síle"), default=0, blank=True, null=True)

    suma_dexterity = models.IntegerField(("Obratnost"), default=1, blank=True, null=True)
    dexterity_base = models.IntegerField(("Základní obratnost"), default=1, blank=True, null=True)
    dexterity_plus = models.IntegerField(("plus k obratnosti"), default=0, blank=True, null=True)

    suma_intelligence = models.IntegerField(("Inteligence"), default=1, blank=True, null=True)
    intelligence_base = models.IntegerField(("Základní inteligence"), default=1, blank=True, null=True)
    intelligence_plus = models.IntegerField(("plus k inteligenci"), default=0, blank=True, null=True)

    suma_charisma = models.IntegerField(("Charisma"), default=1, blank=True, null=True)
    charisma_base = models.IntegerField(("Základní charisma"), default=1, blank=True, null=True)
    charisma_plus = models.IntegerField(("plus k charismatu"), default=0, blank=True, null=True)

    suma_vitality = models.IntegerField(("Vitalita"), default=1, blank=True, null=True)
    vitality_base = models.IntegerField(("Základní vitalita"), default=1, blank=True, null=True)
    vitality_plus = models.IntegerField(("plus k vitalitě"), default=0, blank=True, null=True)

    suma_luck = models.IntegerField(("Zručnost"), default=1, blank=True, null=True)
    luck_base = models.IntegerField(("Základní zručnost"), default=1, blank=True, null=True)
    luck_plus = models.IntegerField(("plus k zručnosti"), default=0, blank=True, null=True)

    dmg_atribut = models.CharField(max_length=20, choices=Playerinfo.ATRIBUTS_CHOICES, blank=True, null=True)

class INV(models.Model):
    hrac = models.ForeignKey(Playerinfo, on_delete=models.CASCADE, related_name='inventory', blank=True)


class EQP(models.Model):
    hrac = models.ForeignKey(Playerinfo, on_delete=models.CASCADE, related_name='equipment', blank=True)


class Character_bonus(models.Model):
    hrac = models.ForeignKey(Playerinfo, on_delete=models.CASCADE, related_name='character_bonus', blank=True)


class ShopOffer(models.Model):
    hrac = models.ForeignKey(Playerinfo, on_delete=models.CASCADE, related_name='shop_offers', blank=True)
    item_id = models.IntegerField(default=1, blank=True)
    item_type = models.CharField(max_length=20, choices=Playerinfo.ITEM_TYPE_CHOICES)
    item_name = models.CharField(max_length=100, blank=True)
    item_price = models.PositiveIntegerField(blank=True, default=1)
    item_description = models.TextField(blank=True)
    item_level_required = models.PositiveIntegerField(blank=True, default=1)
    item_level_stop = models.PositiveIntegerField(blank=True, default=1)
    item_weapon_type = models.CharField(max_length=20, blank=True, default=1)
    item_base_damage = models.PositiveIntegerField(blank=True, default=1)
    item_min_damage = models.PositiveIntegerField(blank=True, default=1)
    item_max_damage = models.PositiveIntegerField(blank=True, default=1)
    item_slots = models.PositiveIntegerField(blank=True, default=1)

    def __str__(self):
        return f"{self.item_name} (Cena: {self.item_price} zlaťáků)"
