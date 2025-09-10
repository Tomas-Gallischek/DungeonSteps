from email.mime import base
from pyexpat import model
from turtle import mode
from urllib import request
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone


# HLAVNÍ DATABÁZE HRÁČE:
class Playerinfo(AbstractUser):
    ITEM_TYPE_CHOICES = (
        ('heavy', 'Těžké'),
        ('light', 'Lehké'),
        ('magic', 'Magické'),
    )

    ITEM_CATEGORY_CHOICES = (
        ('weapon', 'zbraň'),
        ('armor', 'brnění'),
        ('helmet', 'helma'),
        ('boots', 'boty'),
        ('ring', 'prsten'),
        ('amulet', 'náhrdelník'),
        ('talisman', 'talisman'),

    )
    
    GENDER_CHOICES = (
        ('male', 'Muž'),
        ('female', 'Žena'),
        ('other', 'Jiné'),
    )
    RASA_CHOICES = (
        ('human', 'Člověk'),
        ('elf', 'Elf'),
        ('dwarf', 'Trpaslík'),
        ('ork', 'Ork'),
        ('gnóm', 'Gnóm'),
        ('shadow', 'Stín'),
    )
    POVOLANI_CHOICES = (
        ('ranger', 'Hraničář'),
        ('paladin', 'Paladin'),
        ('mage', 'Mág'),
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
    rasa = models.CharField(max_length=20, choices=RASA_CHOICES, blank=True, null=True)
    povolani = models.CharField(max_length=20, choices=POVOLANI_CHOICES, blank=True, null=True)
    item_type = models.CharField(max_length=20, choices=ITEM_TYPE_CHOICES, blank=True, null=True)
    date_joined = models.DateTimeField(default=timezone.now)

def __str__(self):
    return self.username

# VŠECHNY VNOŘENÉ DATABÁZE
class XP_LVL(models.Model):
    hrac = models.OneToOneField(Playerinfo, on_delete=models.CASCADE, related_name='xp_lvl', blank=True)
    lvl = models.IntegerField(("Úroveň"), default=1, blank=True, null=True)
    xp = models.IntegerField(("Zkušenosti"), default=0, blank=True, null=True)
    xp_to_next_lvl = models.IntegerField(("XP do další úrovně"), default=50, blank=True, null=True)
    xp_nasetreno = models.IntegerField(("XP nasetřeno"), default=0, blank=True, null=True)

    def save(self, *args, **kwargs):
        # Nejdřív získáme aktuální hodnotu XP z databáze, pokud instance existuje
        if self.pk is not None:
            old_instance = XP_LVL.objects.get(pk=self.pk)
            # Pokud se hodnota 'xp' změnila, spustíme výpočet
            if old_instance.xp != self.xp:
                self.vypocitej_lvl_a_xp()
        
        # Voláme save metodu nadřazené třídy, která uloží všechny změny
        super().save(*args, **kwargs)

    def vypocitej_lvl_a_xp(self):
        xp = self.xp
        lvl = 0
        xp_to_next_lvl = 0  

        while xp >= xp_to_next_lvl:
            xp_nasetreno = xp - xp_to_next_lvl
            lvl += 1
            if lvl == 1:
                xp_to_next_lvl = 50
            else:
                xp_to_next_lvl = int(xp_to_next_lvl * 1.2)  # Zvýšení potřebného XP o 20%
            xp = xp_nasetreno
            self.xp_nasetreno = xp_nasetreno

        # Aktualizujeme hodnoty přímo na instanci
        self.lvl = lvl
        self.xp_to_next_lvl = xp_to_next_lvl
        self.xp_nasetreno = xp_nasetreno

    def __str__(self):
        return f"XP_LVL(hrac={self.hrac}, lvl={self.lvl}, xp={self.xp})"


class XP_Log(models.Model):
    hrac = models.ForeignKey(Playerinfo, on_delete=models.CASCADE, related_name='xp_log', blank=True)
    xp_record = models.IntegerField(("Získané XP"), default=0, blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"XP_Log(hrac={self.hrac}, xp_record={self.xp_record}, timestamp={self.timestamp})"

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs) # Nejdříve ulož aktuální záznam
        
        # Získání logů pro aktuálního hráče seřazených od nejnovějších
        logs = XP_Log.objects.filter(hrac=self.hrac).order_by('-timestamp')
        
        # Pokud je logů více než 50, začneme mazat ty nejstarší
        if logs.count() > 50:
            old_logs = logs[50:]
            for log in old_logs:
                log.delete()

class Economy(models.Model):
    hrac = models.OneToOneField(Playerinfo, on_delete=models.CASCADE, related_name='economy', blank=True)
    gold = models.IntegerField(("Počet GOLDŮ"), default=1)
    dungeon_token = models.IntegerField(("Počet DUNGEON TOKENŮ"), default=0)

    def __str__(self):
        return f"Economic(hrac={self.hrac}, gold={self.gold}, dungeon_token={self.dungeon_token})"

class Economy_Log(models.Model):
    hrac = models.ForeignKey(Playerinfo, on_delete=models.CASCADE, related_name='economy_log', blank=True)
    gold_change = models.IntegerField(("Změna GOLDŮ"), default=0, blank=True, null=True)
    dungeon_token_change = models.IntegerField(("Změna DUNGEON TOKENŮ"), default=0, blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Economy_Log(hrac={self.hrac}, gold_change={self.gold_change}, dungeon_token_change={self.dungeon_token_change}, timestamp={self.timestamp})"

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        logs = Economy_Log.objects.filter(hrac=self.hrac).order_by('-timestamp')
        
        if logs.count() > 50:
            old_logs = logs[50:]
            for log in old_logs:
                log.delete()

from django.db import models

class Atributs(models.Model):
    hrac = models.OneToOneField(Playerinfo, on_delete=models.CASCADE, related_name='atributy', blank=True, null=True)

# BASE = Rasa + povolání
# PLUS = Zvyšování klikáním
# ITEMS = Bonusy z předmětů (ty sčítat zvlášť v eqp a pak je posílat sem)
# CENA = Výpočet ceny na úrovni databáze zatím pomocí ** 1.5


    suma_hp = models.IntegerField(("Počet životů"), default=100, blank=True, null=True)
    hp_base = models.FloatField(("Bonus k životům"), default=100, blank=True, null=True)
    hp_rasa = models.FloatField(("Životy z rasy"), default=0, blank=True, null=True)
    hp_vit = models.FloatField(("plus k životům"), default=0, blank=True, null=True)
    hp_koeficient = models.FloatField(("Koeficient k životům"), default=1.0, blank=True, null=True)
    hp_bonus_procenta = models.FloatField(("Bonus k životům (%)"), default=0, blank=True, null=True)

    suma_strength = models.IntegerField(("Síla"), default=1, blank=True, null=True)
    strength_base = models.IntegerField(("Základní síla"), default=1, blank=True, null=True)
    strength_plus = models.IntegerField(("plus k síle"), default=0, blank=True, null=True)
    strength_items = models.IntegerField(("Bonus k síle (předměty)"), default=0, blank=True, null=True)

    suma_dexterity = models.IntegerField(("Obratnost"), default=1, blank=True, null=True)
    dexterity_base = models.IntegerField(("Základní obratnost"), default=1, blank=True, null=True)
    dexterity_plus = models.IntegerField(("plus k obratnosti"), default=0, blank=True, null=True)
    dexterity_items = models.IntegerField(("Bonus k obratnosti (předměty)"), default=0, blank=True, null=True)

    suma_intelligence = models.IntegerField(("Inteligence"), default=1, blank=True, null=True)
    intelligence_base = models.IntegerField(("Základní inteligence"), default=1, blank=True, null=True)
    intelligence_plus = models.IntegerField(("plus k inteligenci"), default=0, blank=True, null=True)
    intelligence_items = models.IntegerField(("Bonus k inteligenci (předměty)"), default=0, blank=True, null=True)

    suma_charisma = models.IntegerField(("Charisma"), default=1, blank=True, null=True)
    charisma_base = models.IntegerField(("Základní charisma"), default=1, blank=True, null=True)
    charisma_plus = models.IntegerField(("plus k charismatu"), default=0, blank=True, null=True)
    charisma_items = models.IntegerField(("Bonus k charismatu (předměty)"), default=0, blank=True, null=True)

    suma_vitality = models.IntegerField(("Vitalita"), default=1, blank=True, null=True)
    vitality_base = models.IntegerField(("Základní vitalita"), default=1, blank=True, null=True)
    vitality_plus = models.IntegerField(("plus k vitalitě"), default=0, blank=True, null=True)
    vitality_items = models.IntegerField(("Bonus k vitalitě (předměty)"), default=0, blank=True, null=True)

    suma_luck = models.IntegerField(("Zručnost"), default=1, blank=True, null=True)
    luck_base = models.IntegerField(("Základní zručnost"), default=1, blank=True, null=True)
    luck_plus = models.IntegerField(("plus k zručnosti"), default=0, blank=True, null=True)
    luck_items = models.IntegerField(("Bonus k zručnosti (předměty)"), default=0, blank=True, null=True)

    dmg_atribut = models.CharField(max_length=20, choices=Playerinfo.ATRIBUTS_CHOICES, blank=True, null=True)

    strength_cena = models.IntegerField(("Cena za zvýšení síly"), default=1, blank=True, null=True)
    dexterity_cena = models.IntegerField(("Cena za zvýšení obratnosti"), default=1, blank=True, null=True)
    intelligence_cena = models.IntegerField(("Cena za zvýšení inteligence"), default=1, blank=True, null=True)
    charisma_cena = models.IntegerField(("Cena za zvýšení charismatu"), default=1, blank=True, null=True)
    vitality_cena = models.IntegerField(("Cena za zvýšení vitality"), default=1, blank=True, null=True)
    luck_cena = models.IntegerField(("Cena za zvýšení zručnosti"), default=1, blank=True, null=True)

    def save(self, *args, **kwargs):
    # HP
        self.hp_base = 99 + (XP_LVL.objects.get(hrac=self.hrac).lvl ** 2)
        self.hp_vit = (self.suma_vitality) * (self.suma_vitality / 10)
        self.suma_hp = ((self.hp_base) + (self.hp_vit) + (self.hp_rasa)) * (self.hp_koeficient)
        self.hp_bonus_procenta = (self.hp_vit) / (self.suma_hp / 100)
    # OSTATNÍ ATRIBUTY
        self.suma_strength = self.strength_base + self.strength_plus + self.strength_items
        self.suma_dexterity = self.dexterity_base + self.dexterity_plus + self.dexterity_items
        self.suma_intelligence = self.intelligence_base + self.intelligence_plus + self.intelligence_items
        self.suma_charisma = self.charisma_base + self.charisma_plus + self.charisma_items
        self.suma_vitality = self.vitality_base + self.vitality_plus + self.vitality_items
        self.suma_luck = self.luck_base + self.luck_plus + self.luck_items

    # CENA ZA VYLEPŠENÍ
        self.strength_cena = self.strength_plus ** 1.5
        self.dexterity_cena = self.dexterity_plus ** 1.5
        self.intelligence_cena = self.intelligence_plus ** 1.5
        self.charisma_cena = self.charisma_plus ** 1.5
        self.vitality_cena = self.vitality_plus ** 1.5
        self.luck_cena = self.luck_plus ** 1.5
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Atributy pro hráče {self.hrac.username}"

class Character_bonus(models.Model):
    hrac = models.ForeignKey(Playerinfo, on_delete=models.CASCADE, related_name='character_bonus', blank=True)


class ShopOffer(models.Model):
    hrac = models.ForeignKey(Playerinfo, on_delete=models.CASCADE, related_name='shop_offer', blank=True)
    name = models.CharField(max_length=100, blank=True, null=True)
    item_id = models.IntegerField(default=0, blank=True, null=True)
    img_init = models.CharField(max_length=200, blank=True, null=True)
    description = models.TextField(max_length=500, blank=True, null=True)
    level_required = models.IntegerField(default=1, blank=True, null=True)
    level_stop = models.IntegerField(default=10, blank=True, null=True)
    item_type = models.CharField(max_length=20, choices=Playerinfo.ITEM_TYPE_CHOICES, blank=True, null=True)
    item_category = models.CharField(max_length=20, choices=Playerinfo.ITEM_CATEGORY_CHOICES, blank=True, null=True)

    slots = models.IntegerField(default=0, blank=True, null=True)
    slot_1_bonus = models.CharField(max_length=50, blank=True, null=True)
    slot_1_value = models.IntegerField(blank=True, null=True)
    slot_2_bonus = models.CharField(max_length=50, blank=True, null=True)
    slot_2_value = models.IntegerField(blank=True, null=True)
    slot_3_bonus = models.CharField(max_length=50, blank=True, null=True)
    slot_3_value = models.IntegerField(blank=True, null=True)
    slot_4_bonus = models.CharField(max_length=50, blank=True, null=True)
    slot_4_value = models.IntegerField(blank=True, null=True)

    price = models.IntegerField(default=0)

    min_dmg = models.IntegerField(default=0, blank=True, null=True)
    max_dmg = models.IntegerField(default=1, blank=True, null=True)
    prum_dmg = models.FloatField(default=0, blank=True, null=True)

    armor = models.IntegerField(default=0, blank=True, null=True)

    str_bonus = models.IntegerField(default=0, blank=True, null=True)
    dex_bonus = models.IntegerField(default=0, blank=True, null=True)
    int_bonus = models.IntegerField(default=0, blank=True, null=True)
    vit_bonus = models.IntegerField(default=0, blank=True, null=True)
    luk_bonus = models.IntegerField(default=0, blank=True, null=True)

    def save(self, *args, **kwargs):
        self.img_init = f"{self.name}.png"
        self.prum_dmg = (self.min_dmg + self.max_dmg) / 2
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name
    
class INV(models.Model):
    hrac = models.ForeignKey(Playerinfo, on_delete=models.CASCADE, related_name='inventory', blank=True)
    name = models.CharField(max_length=100, blank=True, null=True)
    item_id = models.IntegerField(default=0, blank=True, null=True)
    img_init = models.CharField(max_length=200, blank=True, null=True)
    description = models.TextField(max_length=500, blank=True, null=True)
    level_required = models.IntegerField(default=1, blank=True, null=True)
    level_stop = models.IntegerField(default=10, blank=True, null=True)
    item_type = models.CharField(max_length=20, choices=Playerinfo.ITEM_TYPE_CHOICES, blank=True, null=True)
    item_category = models.CharField(max_length=20, choices=Playerinfo.ITEM_CATEGORY_CHOICES, blank=True, null=True)

    slots = models.IntegerField(default=0, blank=True, null=True)
    slot_1_bonus = models.CharField(max_length=50, blank=True, null=True)
    slot_1_value = models.IntegerField(blank=True, null=True)
    slot_2_bonus = models.CharField(max_length=50, blank=True, null=True)
    slot_2_value = models.IntegerField(blank=True, null=True)
    slot_3_bonus = models.CharField(max_length=50, blank=True, null=True)
    slot_3_value = models.IntegerField(blank=True, null=True)
    slot_4_bonus = models.CharField(max_length=50, blank=True, null=True)
    slot_4_value = models.IntegerField(blank=True, null=True)

    price = models.IntegerField(default=0)

    min_dmg = models.IntegerField(default=0, blank=True, null=True)
    max_dmg = models.IntegerField(default=1, blank=True, null=True)
    prum_dmg = models.FloatField(default=0, blank=True, null=True)

    armor = models.IntegerField(default=0, blank=True, null=True)

    str_bonus = models.IntegerField(default=0, blank=True, null=True)
    dex_bonus = models.IntegerField(default=0, blank=True, null=True)
    int_bonus = models.IntegerField(default=0, blank=True, null=True)
    vit_bonus = models.IntegerField(default=0, blank=True, null=True)
    luk_bonus = models.IntegerField(default=0, blank=True, null=True)

    def save(self, *args, **kwargs):
        self.img_init = f"{self.name}.png"
        self.prum_dmg = (self.min_dmg + self.max_dmg) / 2
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

class EQP(models.Model):
    hrac = models.ForeignKey(Playerinfo, on_delete=models.CASCADE, related_name='eqp', blank=True, null=True)
    name = models.CharField(max_length=100, blank=True, null=True)
    item_id = models.IntegerField(default=0, blank=True, null=True)
    img_init = models.CharField(max_length=200, blank=True, null=True)
    description = models.TextField(max_length=500, blank=True, null=True)
    level_required = models.IntegerField(default=1, blank=True, null=True)
    level_stop = models.IntegerField(default=10, blank=True, null=True)
    item_type = models.CharField(max_length=20, choices=Playerinfo.ITEM_TYPE_CHOICES, blank=True, null=True)
    item_category = models.CharField(max_length=20, choices=Playerinfo.ITEM_CATEGORY_CHOICES, blank=True, null=True)

    slots = models.IntegerField(default=0, blank=True, null=True)
    slot_1_bonus = models.CharField(max_length=50, blank=True, null=True)
    slot_1_value = models.IntegerField(blank=True, null=True)
    slot_2_bonus = models.CharField(max_length=50, blank=True, null=True)
    slot_2_value = models.IntegerField(blank=True, null=True)
    slot_3_bonus = models.CharField(max_length=50, blank=True, null=True)
    slot_3_value = models.IntegerField(blank=True, null=True)
    slot_4_bonus = models.CharField(max_length=50, blank=True, null=True)
    slot_4_value = models.IntegerField(blank=True, null=True)

    price = models.IntegerField(default=0)

    min_dmg = models.IntegerField(default=0, blank=True, null=True)
    max_dmg = models.IntegerField(default=1, blank=True, null=True)
    prum_dmg = models.FloatField(default=0, blank=True, null=True)

    armor = models.IntegerField(default=0, blank=True, null=True)

    str_bonus = models.IntegerField(default=0, blank=True, null=True)
    dex_bonus = models.IntegerField(default=0, blank=True, null=True)
    int_bonus = models.IntegerField(default=0, blank=True, null=True)
    vit_bonus = models.IntegerField(default=0, blank=True, null=True)
    luk_bonus = models.IntegerField(default=0, blank=True, null=True)

    def save(self, *args, **kwargs):
        self.img_init = f"{self.name}.png"
        self.prum_dmg = (self.min_dmg + self.max_dmg) / 2
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name