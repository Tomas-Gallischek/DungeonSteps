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
    rasa = models.CharField(max_length=20, choices=RASA_CHOICES, blank=True, null=True)
    povolani = models.CharField(max_length=20, choices=POVOLANI_CHOICES, blank=True, null=True)

def __str__(self):
    return self.username

# VŠECHNY VNOŘENÉ DATABÁZE
class XP_LVL(models.Model):
    hrac = models.OneToOneField(Playerinfo, on_delete=models.CASCADE, related_name='xp_lvl', blank=True)
    lvl = models.IntegerField(("Úroveň"), default=0, blank=True, null=True)
    xp = models.IntegerField(("Zkušenosti"), default=0, blank=True, null=True)
    xp_to_next_lvl = models.IntegerField(("XP do další úrovně"), default=0, blank=True, null=True)
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

class Economy(models.Model):
    hrac = models.OneToOneField(Playerinfo, on_delete=models.CASCADE, related_name='economy', blank=True)
    gold = models.IntegerField(("Počet GOLDŮ"), default=1)
    rohlik = models.IntegerField(("Počet ROHLÍKŮ"), default=1)
    gold_growth_coefficient = models.FloatField(("Koeficient růstu GOLDŮ"), default=1.0)
    last_gold_collection = models.DateTimeField(blank=True, null=True, default=timezone.now)
    dungeon_token = models.IntegerField(("Počet DUNGEON TOKENŮ"), default=0)

    def __str__(self):
        return f"Economic(hrac={self.hrac}, gold={self.gold}, rohlik={self.rohlik}, gold_growth_coefficient={self.gold_growth_coefficient}, last_gold_collection={self.last_gold_collection})"

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

    def __str__(self):
        return f"Atributs(hrac={self.hrac}, HP={self.HP}, hp_bonus={self.hp_bonus}, suma_strength={self.suma_strength}, strength_base={self.strength_base}, strength_plus={self.strength_plus}, suma_dexterity={self.suma_dexterity}, dexterity_base={self.dexterity_base}, dexterity_plus={self.dexterity_plus}, suma_intelligence={self.suma_intelligence}, intelligence_base={self.intelligence_base}, intelligence_plus={self.intelligence_plus}, suma_charisma={self.suma_charisma}, charisma_base={self.charisma_base}, charisma_plus={self.charisma_plus}, suma_vitality={self.suma_vitality}, vitality_base={self.vitality_base}, vitality_plus={self.vitality_plus}, suma_luck={self.suma_luck}, luck_base={self.luck_base}, luck_plus={self.luck_plus}, dmg_atribut={self.dmg_atribut})"

class Character_bonus(models.Model):
    hrac = models.ForeignKey(Playerinfo, on_delete=models.CASCADE, related_name='character_bonus', blank=True)


class ShopOffer(models.Model):
    hrac = models.ForeignKey(Playerinfo, on_delete=models.CASCADE, related_name='shop_offers', blank=True)
    item_id = models.IntegerField(default=1, blank=True)
    item_type = models.CharField(max_length=20, choices=Playerinfo.ITEM_TYPE_CHOICES, blank=True)
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
    
class INV(models.Model):
    hrac = models.ForeignKey(Playerinfo, on_delete=models.CASCADE, related_name='inventory', blank=True)
    item_id = models.IntegerField(default=1, blank=True)
    item_type = models.CharField(max_length=20, choices=Playerinfo.ITEM_TYPE_CHOICES, blank=True)
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

class EQP(models.Model):
    hrac = models.ForeignKey(Playerinfo, on_delete=models.CASCADE, related_name='equipment', blank=True)
    item_id = models.IntegerField(default=1, blank=True)
    item_type = models.CharField(max_length=20, choices=Playerinfo.ITEM_TYPE_CHOICES, blank=True)
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