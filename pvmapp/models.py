from math import floor
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
from django.db.models import Sum

ATRIBUTS_CHOICES = (
    ('strength', 'Síla'),
    ('dexterity', 'Obratnost'),
    ('intelligence', 'Inteligence'),
    ('luck', 'Štěstí'),
    ('vitality', 'Vitalita'),
    ('none', 'Žádný')
)

class Mobs_random(models.Model):

    mob_id = models.IntegerField(("ID Monstra"), unique=True)
    name = models.CharField(max_length=100)
    img = models.ImageField(upload_to='mobs_images/', blank=True, null=True)
    description = models.TextField(("Popis"), blank=True, null=True)
    locations = models.TextField(("Lokace"), blank=True, null=True)

# časem implementovat
    gold_loot_bonus = models.FloatField(("Bonus ke zlatým"), default=0, blank=True, null=True)
    xp_loot_bonus = models.FloatField(("Bonus k XP"), default=0, blank=True, null=True)
    items_loot_bonus = models.FloatField(("Bonus k předmětům"), default=0, blank=True, null=True)


    def __str__(self):
        return self.name    
    

class Mobs_dungeons(models.Model):

    dungeon = models.IntegerField(("Číslo Dungeonu"), blank=True, null=True)
    floor = models.IntegerField(("Patro Dungeonu"), blank=True, null=True)

    name = models.CharField(max_length=100)
    mob_id = models.IntegerField(("ID Monstra"), unique=True)
    img = models.ImageField(upload_to='mobs_images/', blank=True, null=True)
    description = models.TextField(("Popis"), blank=True, null=True)
    dificulty_koeficient = models.IntegerField(("Obtížnost"), default=1, blank=True, null=True)
    lvl = models.IntegerField(("Úroveň"), default=1, blank=True, null=True)

    gold_loot_bonus = models.FloatField(("Bonus ke zlatým"), default=0, blank=True, null=True)
    xp_loot_bonus = models.FloatField(("Bonus k XP"), default=0, blank=True, null=True)
    items_loot_bonus = models.FloatField(("Bonus k předmětům"), default=0, blank=True, null=True)

    hp = models.FloatField(("Životy"), default=1, blank=True, null=True)
    str = models.FloatField(("Síla"), default=1, blank=True, null=True)
    dex = models.FloatField(("Obratnost"), default=1, blank=True, null=True)
    int = models.FloatField(("Inteligence"), default=1, blank=True, null=True)
    vit = models.FloatField(("Vitalita"), default=1, blank=True, null=True)
    luck = models.FloatField(("Štěstí"), default=1, blank=True, null=True)

    dmg_atr = models.CharField(max_length=100, choices=ATRIBUTS_CHOICES, default='none')

    magic_resist = models.FloatField(("Magická odolnost"), default=0, blank=True, null=True)
    light_resist = models.FloatField(("Lehká odolnost"), default=0, blank=True, null=True)
    heavy_resist = models.FloatField(("Těžká odolnost"), default=0, blank=True, null=True)
    otrava_resist = models.FloatField(("Otrava odolnost"), default=0, blank=True, null=True)
    bezvedomi_resist = models.FloatField(("Bezvědomí odolnost"), default=0, blank=True, null=True)

    poskozeni_schopnosti = models.FloatField(("Poškození schopností"), default=0, blank=True, null=True)
    poskozeni_utokem = models.FloatField(("Poškození útokem"), default=0, blank=True, null=True)
    sance_na_otravu = models.FloatField(("Šance na otravu"), default=0, blank=True, null=True)
    sance_na_bezvedomi = models.FloatField(("Šance na bezvědomí"), default=0, blank=True, null=True)

    sance_na_kriticky_utok = models.FloatField(("Šance na kritický útok"), default=0, blank=True, null=True)
    kriticke_poskozeni = models.FloatField(("Kritické poškození"), default=0, blank=True, null=True)

    armor = models.FloatField(("Brnění"), default=0, blank=True, null=True)

    min_dmg = models.FloatField(("Minimální poškození"), default=1, blank=True, null=True)
    max_dmg = models.FloatField(("Maximální poškození"), default=1, blank=True, null=True)


    def __str__(self):
        return self.name    