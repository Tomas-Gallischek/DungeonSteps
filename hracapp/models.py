from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
from django.db.models import Sum

# HLAVNÍ DATABÁZE HRÁČE:
class Playerinfo(AbstractUser):
    ITEM_TYPE_CHOICES = (
        ('universal', 'Univerzální'),
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
        # Tady nastává chyba, pokud self.hrac == None
        # return f"XP_LVL(hrac={self.hrac}, lvl={self.lvl}, xp={self.xp})"

        # Zabezpečená verze: Zobrazí username, pokud existuje, jinak ID
        if self.hrac:
            hrac_info = self.hrac.username
        else:
            hrac_info = f'Žádný hráč (ID: {self.id})'
            
        return f"XP_LVL(hrac={hrac_info}, lvl={self.lvl}, xp={self.xp})"


class XP_Log(models.Model):
    hrac = models.ForeignKey(Playerinfo, on_delete=models.CASCADE, related_name='xp_log', blank=True)
    xp_record = models.IntegerField(("Získané XP"), default=0, blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs) # Nejdříve ulož aktuální záznam
        
        # Získání logů pro aktuálního hráče seřazených od nejnovějších
        logs = XP_Log.objects.filter(hrac=self.hrac).order_by('-timestamp')
        
        # Pokud je logů více než 50, začneme mazat ty nejstarší
        if logs.count() > 50:
            old_logs = logs[50:]
            for log in old_logs:
                log.delete()
    
    def __str__(self):

        if self.hrac:
            hrac_info = self.hrac.username
        else:
            hrac_info = f'Žádný hráč (ID: {self.id})'

        return f"XP_Log(hrac={hrac_info}, xp_record={self.xp_record}, timestamp={self.timestamp})"

class Economy(models.Model):
    hrac = models.OneToOneField(Playerinfo, on_delete=models.CASCADE, related_name='economy', blank=True)
    gold = models.IntegerField(("Počet GOLDŮ"), default=1)
    dungeon_token = models.IntegerField(("Počet DUNGEON TOKENŮ"), default=0)

    def __str__(self):

        if self.hrac:
            hrac_info = self.hrac.username
        else:
            hrac_info = f'Žádný hráč (ID: {self.id})'
        return f"Economy(hrac={hrac_info}, gold={self.gold}, dungeon_token={self.dungeon_token})"

class Economy_Log(models.Model):
    hrac = models.ForeignKey(Playerinfo, on_delete=models.CASCADE, related_name='economy_log', blank=True)
    gold_change = models.IntegerField(("Změna GOLDŮ"), default=0, blank=True, null=True)
    dungeon_token_change = models.IntegerField(("Změna DUNGEON TOKENŮ"), default=0, blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):

        if self.hrac:
            hrac_info = self.hrac.username
        else:
            hrac_info = f'Žádný hráč (ID: {self.id})'

        return f"Economy_Log(hrac={hrac_info}, gold_change={self.gold_change}, dungeon_token_change={self.dungeon_token_change}, timestamp={self.timestamp})"

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        logs = Economy_Log.objects.filter(hrac=self.hrac).order_by('-timestamp')
        
        if logs.count() > 50:
            old_logs = logs[50:]
            for log in old_logs:
                log.delete()

class Atributs(models.Model):
    hrac = models.OneToOneField(Playerinfo, on_delete=models.CASCADE, related_name='atributy', blank=True, null=True)

# BASE = Rasa + povolání
# PLUS = Zvyšování klikáním
# ITEMS = Bonusy z předmětů
# CENA = Výpočet ceny na úrovni databáze zatím pomocí ** 1.5


    suma_hp = models.IntegerField(("Počet životů"), default=100, blank=True, null=True)
    hp_base = models.FloatField(("Bonus k životům"), default=100, blank=True, null=True)
    hp_rasa = models.FloatField(("Životy z rasy"), default=0, blank=True, null=True)
    hp_vit = models.FloatField(("plus k životům"), default=0, blank=True, null=True)
    hp_items = models.FloatField(("Bonus k životům (předměty)"), default=0, blank=True, null=True)
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

    suma_vitality = models.IntegerField(("Vitalita"), default=1, blank=True, null=True)
    vitality_base = models.IntegerField(("Základní vitalita"), default=1, blank=True, null=True)
    vitality_plus = models.IntegerField(("plus k vitalitě"), default=0, blank=True, null=True)
    vitality_items = models.IntegerField(("Bonus k vitalitě (předměty)"), default=0, blank=True, null=True)

    suma_luck = models.IntegerField(("Zručnost"), default=1, blank=True, null=True)
    luck_base = models.IntegerField(("Základní štěstí"), default=1, blank=True, null=True)
    luck_plus = models.IntegerField(("plus k štěstí"), default=0, blank=True, null=True)
    luck_items = models.IntegerField(("Bonus k štěstí (předměty)"), default=0, blank=True, null=True)

    dmg_atribut = models.CharField(max_length=20, choices=Playerinfo.ATRIBUTS_CHOICES, blank=True, null=True)

    strength_cena = models.IntegerField(("Cena za zvýšení síly"), default=1, blank=True, null=True)
    dexterity_cena = models.IntegerField(("Cena za zvýšení obratnosti"), default=1, blank=True, null=True)
    intelligence_cena = models.IntegerField(("Cena za zvýšení inteligence"), default=1, blank=True, null=True)
    vitality_cena = models.IntegerField(("Cena za zvýšení vitality"), default=1, blank=True, null=True)
    luck_cena = models.IntegerField(("Cena za zvýšení štěstí"), default=1, blank=True, null=True)

    def save(self, *args, **kwargs):
    # HP
        self.hp_base = 99 + (XP_LVL.objects.get(hrac=self.hrac).lvl ** 2)
        self.hp_vit = (self.suma_vitality) * (self.suma_vitality / 10)
        self.hp_items = Character_bonus.objects.get(hrac=self.hrac).hp_flat_it_bonus
        self.suma_hp = ((self.hp_base) + (self.hp_vit) + (self.hp_rasa) + (self.hp_items)) * (self.hp_koeficient)
        self.hp_bonus_procenta = (self.hp_vit) / (self.suma_hp / 100)

    # ATRIBUTY Z VYBAVENÍ
        self.strength_items = Character_bonus.objects.get(hrac=self.hrac).str_flat_it_bonus + Character_bonus.objects.get(hrac=self.hrac).str_bonus
        self.dexterity_items = Character_bonus.objects.get(hrac=self.hrac).dex_flat_it_bonus + Character_bonus.objects.get(hrac=self.hrac).dex_bonus
        self.intelligence_items = Character_bonus.objects.get(hrac=self.hrac).int_flat_it_bonus + Character_bonus.objects.get(hrac=self.hrac).int_bonus
        self.vitality_items = Character_bonus.objects.get(hrac=self.hrac).vit_flat_it_bonus + Character_bonus.objects.get(hrac=self.hrac).vit_bonus
        self.luck_items = Character_bonus.objects.get(hrac=self.hrac).luck_flat_it_bonus + Character_bonus.objects.get(hrac=self.hrac).luk_bonus

    # OSTATNÍ ATRIBUTY
        self.suma_strength = self.strength_base + self.strength_plus + self.strength_items
        self.suma_dexterity = self.dexterity_base + self.dexterity_plus + self.dexterity_items
        self.suma_intelligence = self.intelligence_base + self.intelligence_plus + self.intelligence_items
        self.suma_vitality = self.vitality_base + self.vitality_plus + self.vitality_items
        self.suma_luck = self.luck_base + self.luck_plus + self.luck_items

    # CENA ZA VYLEPŠENÍ
        self.strength_cena = self.strength_plus ** 1.5
        self.dexterity_cena = self.dexterity_plus ** 1.5
        self.intelligence_cena = self.intelligence_plus ** 1.5
        self.vitality_cena = self.vitality_plus ** 1.5
        self.luck_cena = self.luck_plus ** 1.5
        super().save(*args, **kwargs)

    def __str__(self):

        if self.hrac:
            hrac_info = self.hrac.username
        else:
            hrac_info = f'Žádný hráč (ID: {self.id})'

        return f"Atributy pro hráče {hrac_info}"


class Character_bonus(models.Model):
    hrac = models.ForeignKey(Playerinfo, on_delete=models.CASCADE, related_name='char_bonus', blank=True)
    
    # NOVÉ SLUPCE, KTERÉ JSI CHTĚL PŘIDAT
    str_bonus = models.IntegerField(default=0, blank=True, null=True, verbose_name="Bonus k síle")
    dex_bonus = models.IntegerField(default=0, blank=True, null=True, verbose_name="Bonus k obratnosti")
    int_bonus = models.IntegerField(default=0, blank=True, null=True, verbose_name="Bonus k inteligenci")
    vit_bonus = models.IntegerField(default=0, blank=True, null=True, verbose_name="Bonus k vitalitě")
    luk_bonus = models.IntegerField(default=0, blank=True, null=True, verbose_name="Bonus ke zručnosti")
    
    # STÁVAJÍCÍ SLUPCE
    hp_flat_it_bonus = models.FloatField(("Bonus k životům (předměty)"), default=0, blank=True, null=True)
    pvm_resist_procent_it_bonus = models.FloatField(("Procentuální odolnost proti PVM (předměty)"), default=0, blank=True, null=True)
    pvp_resist_procenta_it_bonus = models.FloatField(("Procentuální odolnost proti PVP (předměty)"), default=0, blank=True, null=True)

    magic_resist_procenta_it_bonus = models.FloatField(("Procentuální odolnost proti magii (předměty)"), default=0, blank=True, null=True)
    heavy_resist_procenta_it_bonus = models.FloatField(("Procentuální odolnost proti těžkým zbraním (předměty)"), default=0, blank=True, null=True)
    light_resist_procenta_it_bonus = models.FloatField(("Procentuální odolnost proti lehkým zbraním (předměty)"), default=0, blank=True, null=True)
    
    otrava_resist_procenta_it_bonus = models.FloatField(("Procentuální odolnost proti otravě (předměty)"), default=0, blank=True, null=True)
    bezvedomi_resist_procenta_it_bonus = models.FloatField(("Procentuální odolnost proti bezvědomí (předměty)"), default=0, blank=True, null=True)

    luck_flat_it_bonus = models.FloatField(("Bonus ke zručnosti (předměty)"), default=0, blank=True, null=True)
    str_flat_it_bonus = models.FloatField(("Bonus k síle (předměty)"), default=0, blank=True, null=True)
    dex_flat_it_bonus = models.FloatField(("Bonus k obratnosti (předměty)"), default=0, blank=True, null=True)
    int_flat_it_bonus = models.FloatField(("Bonus k inteligenci (předměty)"), default=0, blank=True, null=True)
    vit_flat_it_bonus = models.FloatField(("Bonus k vitalitě (předměty)"), default=0, blank=True, null=True)
    
    pvm_poskozeni_procenta_it_bonus = models.FloatField(("Procentuální bonus k poškození proti PVM (předměty)"), default=0, blank=True, null=True)
    pvp_poskozeni_procenta_it_bonus = models.FloatField(("Procentuální bonus k poškození proti PVP (předměty)"), default=0, blank=True, null=True)
    poskozeni_schopnosti_procenta_it_bonus = models.FloatField(("Procentuální bonus k poškození ze schopností (předměty)"), default=0, blank=True, null=True)
    poskozeni_utokem_procenta_it_bonus = models.FloatField(("Procentuální bonus k poškození z útoku (předměty)"), default=0, blank=True, null=True)
    sance_na_otravu_procenta_it_bonus = models.FloatField(("Procentuální šance na otravu (předměty)"), default=0, blank=True, null=True)
    sance_na_bezvedomi_procenta_it_bonus = models.FloatField(("Procentuální šance na bezvědomí (předměty)"), default=0, blank=True, null=True)
    kriticke_poskozeni_procenta_it_bonus = models.FloatField(("Procentuální bonus ke kritickému poškození (předměty)"), default=0, blank=True, null=True)

    armor_armor = models.IntegerField(("Hodnota brnění (předměty)"), default=0, blank=True, null=True)
    armor_helmet = models.IntegerField(("Hodnota helmy (předměty)"), default=0, blank=True, null=True)
    armor_boots = models.IntegerField(("Hodnota bot (předměty)"), default=0, blank=True, null=True)
    armor_suma = models.IntegerField(("Celková hodnota brnění (předměty)"), default=0, blank=True, null=True)

    def save(self, *args, **kwargs):
        # ... (zbytek metody je stejný, ale bez suma výpočtů a dotazů na atributy)

        # Seznam všech polí, které chceme sečíst
        bonus_fields = [
            # ... (všechny původní bonus_fields)
            'hp_flat_it_bonus', 'pvm_resist_procenta_it_bonus', 'pvp_resist_procenta_it_bonus',
            'magic_resist_procenta_it_bonus', 'heavy_resist_procenta_it_bonus', 'light_resist_procenta_it_bonus',
            'otrava_resist_procenta_it_bonus', 'bezvedomi_resist_procenta_it_bonus', 'luck_flat_it_bonus',
            'str_flat_it_bonus', 'dex_flat_it_bonus', 'int_flat_it_bonus', 'vit_flat_it_bonus',
            'pvm_poskozeni_procenta_it_bonus', 'pvp_poskozeni_procenta_it_bonus',
            'poskozeni_schopnosti_procenta_it_bonus', 'poskozeni_utokem_procenta_it_bonus',
            'sance_na_otravu_procenta_it_bonus', 'sance_na_bezvedomi_procenta_it_bonus',
            'kriticke_poskozeni_procenta_it_bonus',
            
            # NOVÉ NÁZVY POLÍ, KTERÉ PŘIDÁVÁME
            'str_bonus', 'dex_bonus', 'int_bonus', 'vit_bonus', 'luk_bonus'
        ]

        # Vytvoření slovníku s argumenty pro agregaci
        aggregation_kwargs = {f'{field}__sum': Sum(field) for field in bonus_fields}

        # Jeden efektivní dotaz na databázi, který sečte vše najednou
        bonuses = EQP.objects.filter(hrac=self.hrac).aggregate(**aggregation_kwargs)

        # Přiřazení sečtených hodnot k polím modelu, s ošetřením hodnot None
        for field in bonus_fields:
            sum_value = bonuses.get(f'{field}__sum')
            setattr(self, field, sum_value or 0)

        super().save(*args, **kwargs)


# SUPER VYCHITÁVKA OD GEMINI --- UMOŽŇUJE VYTVOŘIRT PROMĚNNOU KTERÁ SE VOLÁ ÚPLNĚ STEJNĚ JAKO ZÁZNAM V DATABÁZI ALE NENÍ TAM NAPEVNO 
    @property
    def magic_resist_atr_bonus(self):
        try:
            lvl = XP_LVL.objects.get(hrac=self.hrac).lvl
            return Atributs.objects.get(hrac=self.hrac).suma_intelligence / lvl if lvl != 0 else 0
        except (XP_LVL.DoesNotExist, Atributs.DoesNotExist):
            return 0

    @property
    def heavy_resist_atr_bonus(self):
        try:
            lvl = XP_LVL.objects.get(hrac=self.hrac).lvl
            return Atributs.objects.get(hrac=self.hrac).suma_strength / lvl if lvl != 0 else 0
        except (XP_LVL.DoesNotExist, Atributs.DoesNotExist):
            return 0
    
    @property
    def light_resist_atr_bonus(self):
        try:
            lvl = XP_LVL.objects.get(hrac=self.hrac).lvl
            return Atributs.objects.get(hrac=self.hrac).suma_dexterity / lvl if lvl != 0 else 0
        except (XP_LVL.DoesNotExist, Atributs.DoesNotExist):
            return 0

    @property
    def suma_magic_resist(self):
        return self.magic_resist_procenta_it_bonus + self.magic_resist_atr_bonus

    @property
    def suma_heavy_resist(self):
        return self.heavy_resist_procenta_it_bonus + self.heavy_resist_atr_bonus

    @property
    def suma_light_resist(self):
        return self.light_resist_procenta_it_bonus + self.light_resist_atr_bonus

    def __str__(self):
        # ... (zbytek metody je stejný)
        if self.hrac:
            hrac_info = self.hrac.username
        else:
            hrac_info = f'Žádný hráč (ID: {self.id})'

        return f"Bonusy pro hráče {hrac_info}"
    

class ShopOffer(models.Model):
    hrac = models.ForeignKey(Playerinfo, on_delete=models.CASCADE, related_name='shop_offer', blank=True)
    name = models.CharField(max_length=100, blank=True, null=True)
    item_id = models.IntegerField(default=0, blank=True, null=True)
    img_init = models.CharField(max_length=200, blank=True, null=True)
    description = models.TextField(max_length=500, blank=True, null=True)
    level_required = models.IntegerField(default=1, blank=True, null=True)
    level_stop = models.IntegerField(default=10, blank=True, null=True)
    item_type = models.CharField(max_length=20, choices=Playerinfo.ITEM_TYPE_CHOICES, blank=True, null=True)
    item_category = models.CharField(max_length=20, choices=Playerinfo.ITEM_CATEGORY_CHOICES, blank=True, null=True, default="")
    slots = models.IntegerField(default=0, blank=True, null=True)

    hp_flat_it_bonus = models.FloatField(("Bonus k životům (předměty)"), default=0, blank=True, null=True)
    pvm_resist_procenta_it_bonus = models.FloatField(("Procentuální odolnost proti PVM (předměty)"), default=0, blank=True, null=True)
    pvp_resist_procenta_it_bonus = models.FloatField(("Procentuální odolnost proti PVP (předměty)"), default=0, blank=True, null=True)
    magic_resist_procenta_it_bonus = models.FloatField(("Procentuální odolnost proti magii (předměty)"), default=0, blank=True, null=True)
    heavy_resist_procenta_it_bonus = models.FloatField(("Procentuální odolnost proti těžkým zbraním (předměty)"), default=0, blank=True, null=True)
    light_resist_procenta_it_bonus = models.FloatField(("Procentuální odolnost proti lehkým zbraním (předměty)"), default=0, blank=True, null=True)
    otrava_resist_procenta_it_bonus = models.FloatField(("Procentuální odolnost proti otravě (předměty)"), default=0, blank=True, null=True)
    bezvedomi_resist_procenta_it_bonus = models.FloatField(("Procentuální odolnost proti bezvědomí (předměty)"), default=0, blank=True, null=True)
    luck_flat_it_bonus = models.FloatField(("Bonus ke zručnosti (předměty)"), default=0, blank=True, null=True)
    str_flat_it_bonus = models.FloatField(("Bonus k síle (předměty)"), default=0, blank=True, null=True)
    dex_flat_it_bonus = models.FloatField(("Bonus k obratnosti (předměty)"), default=0, blank=True, null=True)
    int_flat_it_bonus = models.FloatField(("Bonus k inteligenci (předměty)"), default=0, blank=True, null=True)
    vit_flat_it_bonus = models.FloatField(("Bonus k vitalitě (předměty)"), default=0, blank=True, null=True)
    pvm_poskozeni_procenta_it_bonus = models.FloatField(("Procentuální bonus k poškození proti PVM (předměty)"), default=0, blank=True, null=True)
    pvp_poskozeni_procenta_it_bonus = models.FloatField(("Procentuální bonus k poškození proti PVP (předměty)"), default=0, blank=True, null=True)
    poskozeni_schopnosti_procenta_it_bonus = models.FloatField(("Procentuální bonus k poškození ze schopností (předměty)"), default=0, blank=True, null=True)
    poskozeni_utokem_procenta_it_bonus = models.FloatField(("Procentuální bonus k poškození z útoku (předměty)"), default=0, blank=True, null=True)
    sance_na_otravu_procenta_it_bonus = models.FloatField(("Procentuální šance na otravu (předměty)"), default=0, blank=True, null=True)
    sance_na_bezvedomi_procenta_it_bonus = models.FloatField(("Procentuální šance na bezvědomí (předměty)"), default=0, blank=True, null=True)
    kriticke_poskozeni_procenta_it_bonus = models.FloatField(("Procentuální bonus ke kritickému poškození (předměty)"), default=0, blank=True, null=True)

    price = models.IntegerField(default=0)
    sell_price = models.FloatField(("Prodejní cena"), default=0)

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
        super().save(*args, **kwargs)

    def __str__(self):

        if self.hrac:
            hrac_info = self.hrac.username
        else:
            hrac_info = f'Žádný hráč (ID: {self.id})'

        return f"Atributy pro hráče {hrac_info}"

class INV(models.Model):
    hrac = models.ForeignKey(Playerinfo, on_delete=models.CASCADE, related_name='inventory', blank=True)
    name = models.CharField(max_length=100, blank=True, null=True)
    item_id = models.IntegerField(default=0, blank=True, null=True)
    img_init = models.CharField(max_length=200, blank=True, null=True)
    description = models.TextField(max_length=500, blank=True, null=True)
    level_required = models.IntegerField(default=1, blank=True, null=True)
    level_stop = models.IntegerField(default=10, blank=True, null=True)
    item_type = models.CharField(max_length=20, choices=Playerinfo.ITEM_TYPE_CHOICES, blank=True, null=True)
    item_category = models.CharField(max_length=20, choices=Playerinfo.ITEM_CATEGORY_CHOICES, blank=True, null=True, default="")
    slots = models.IntegerField(default=0, blank=True, null=True)

    price = models.IntegerField(default=0)
    sell_price = models.FloatField(("Prodejní cena"), default=0)

    luck_flat_it_bonus = models.FloatField(("Bonus ke zručnosti (předměty)"), default=0, blank=True, null=True)
    str_flat_it_bonus = models.FloatField(("Bonus k síle (předměty)"), default=0, blank=True, null=True)
    dex_flat_it_bonus = models.FloatField(("Bonus k obratnosti (předměty)"), default=0, blank=True, null=True)
    int_flat_it_bonus = models.FloatField(("Bonus k inteligenci (předměty)"), default=0, blank=True, null=True)
    vit_flat_it_bonus = models.FloatField(("Bonus k vitalitě (předměty)"), default=0, blank=True, null=True)
    str_bonus = models.IntegerField(default=0, blank=True, null=True)
    dex_bonus = models.IntegerField(default=0, blank=True, null=True)
    int_bonus = models.IntegerField(default=0, blank=True, null=True)
    vit_bonus = models.IntegerField(default=0, blank=True, null=True)
    luk_bonus = models.IntegerField(default=0, blank=True, null=True)


    hp_flat_it_bonus = models.FloatField(("Bonus k životům (předměty)"), default=0, blank=True, null=True)
    pvm_resist_procenta_it_bonus = models.FloatField(("Procentuální odolnost proti PVM (předměty)"), default=0, blank=True, null=True)
    pvp_resist_procenta_it_bonus = models.FloatField(("Procentuální odolnost proti PVP (předměty)"), default=0, blank=True, null=True)
    magic_resist_procenta_it_bonus = models.FloatField(("Procentuální odolnost proti magii (předměty)"), default=0, blank=True, null=True)
    heavy_resist_procenta_it_bonus = models.FloatField(("Procentuální odolnost proti těžkým zbraním (předměty)"), default=0, blank=True, null=True)
    light_resist_procenta_it_bonus = models.FloatField(("Procentuální odolnost proti lehkým zbraním (předměty)"), default=0, blank=True, null=True)
    otrava_resist_procenta_it_bonus = models.FloatField(("Procentuální odolnost proti otravě (předměty)"), default=0, blank=True, null=True)
    bezvedomi_resist_procenta_it_bonus = models.FloatField(("Procentuální odolnost proti bezvědomí (předměty)"), default=0, blank=True, null=True)
    pvm_poskozeni_procenta_it_bonus = models.FloatField(("Procentuální bonus k poškození proti PVM (předměty)"), default=0, blank=True, null=True)
    pvp_poskozeni_procenta_it_bonus = models.FloatField(("Procentuální bonus k poškození proti PVP (předměty)"), default=0, blank=True, null=True)
    poskozeni_schopnosti_procenta_it_bonus = models.FloatField(("Procentuální bonus k poškození ze schopností (předměty)"), default=0, blank=True, null=True)
    poskozeni_utokem_procenta_it_bonus = models.FloatField(("Procentuální bonus k poškození z útoku (předměty)"), default=0, blank=True, null=True)
    sance_na_otravu_procenta_it_bonus = models.FloatField(("Procentuální šance na otravu (předměty)"), default=0, blank=True, null=True)
    sance_na_bezvedomi_procenta_it_bonus = models.FloatField(("Procentuální šance na bezvědomí (předměty)"), default=0, blank=True, null=True)
    kriticke_poskozeni_procenta_it_bonus = models.FloatField(("Procentuální bonus ke kritickému poškození (předměty)"), default=0, blank=True, null=True)


    min_dmg = models.IntegerField(default=0, blank=True, null=True)
    max_dmg = models.IntegerField(default=1, blank=True, null=True)
    prum_dmg = models.FloatField(default=0, blank=True, null=True)

    armor = models.IntegerField(default=0, blank=True, null=True)



    def save(self, *args, **kwargs):
        # Nejprve ulož samotný předmět
        super().save(*args, **kwargs)

        # --- přepočítání Character_bonus ---
        from .models import Character_bonus, Atributs  # import uvnitř kvůli cyklickým závislostem

        if self.hrac:
            char_bonus, created = Character_bonus.objects.get_or_create(hrac=self.hrac)
            char_bonus.save()  # přepočítá bonusy z EQP + INV

            # --- přepočítání Atributs ---
            atributy, created = Atributs.objects.get_or_create(hrac=self.hrac)
            atributy.save()

    def __str__(self):
        return f"{self.name} ({self.hrac})"

class EQP(models.Model):
    hrac = models.ForeignKey(Playerinfo, on_delete=models.CASCADE, related_name='eqp', blank=True, null=True)
    name = models.CharField(max_length=100, blank=True, null=True)
    item_id = models.IntegerField(default=0, blank=True, null=True)
    img_init = models.CharField(max_length=200, blank=True, null=True)
    description = models.TextField(max_length=500, blank=True, null=True)
    level_required = models.IntegerField(default=1, blank=True, null=True)
    level_stop = models.IntegerField(default=10, blank=True, null=True)
    item_type = models.CharField(max_length=20, choices=Playerinfo.ITEM_TYPE_CHOICES, blank=True, null=True)
    item_category = models.CharField(max_length=20, choices=Playerinfo.ITEM_CATEGORY_CHOICES, blank=True, null=True, default="")
    slots = models.IntegerField(default=0, blank=True, null=True)

    hp_flat_it_bonus = models.FloatField(("Bonus k životům (předměty)"), default=0, blank=True, null=True)
    pvm_resist_procenta_it_bonus = models.FloatField(("Procentuální odolnost proti PVM (předměty)"), default=0, blank=True, null=True)
    pvp_resist_procenta_it_bonus = models.FloatField(("Procentuální odolnost proti PVP (předměty)"), default=0, blank=True, null=True)
    magic_resist_procenta_it_bonus = models.FloatField(("Procentuální odolnost proti magii (předměty)"), default=0, blank=True, null=True)
    heavy_resist_procenta_it_bonus = models.FloatField(("Procentuální odolnost proti těžkým zbraním (předměty)"), default=0, blank=True, null=True)
    light_resist_procenta_it_bonus = models.FloatField(("Procentuální odolnost proti lehkým zbraním (předměty)"), default=0, blank=True, null=True)
    otrava_resist_procenta_it_bonus = models.FloatField(("Procentuální odolnost proti otravě (předměty)"), default=0, blank=True, null=True)
    bezvedomi_resist_procenta_it_bonus = models.FloatField(("Procentuální odolnost proti bezvědomí (předměty)"), default=0, blank=True, null=True)
    luck_flat_it_bonus = models.FloatField(("Bonus ke zručnosti (předměty)"), default=0, blank=True, null=True)
    str_flat_it_bonus = models.FloatField(("Bonus k síle (předměty)"), default=0, blank=True, null=True)
    dex_flat_it_bonus = models.FloatField(("Bonus k obratnosti (předměty)"), default=0, blank=True, null=True)
    int_flat_it_bonus = models.FloatField(("Bonus k inteligenci (předměty)"), default=0, blank=True, null=True)
    vit_flat_it_bonus = models.FloatField(("Bonus k vitalitě (předměty)"), default=0, blank=True, null=True)
    pvm_poskozeni_procenta_it_bonus = models.FloatField(("Procentuální bonus k poškození proti PVM (předměty)"), default=0, blank=True, null=True)
    pvp_poskozeni_procenta_it_bonus = models.FloatField(("Procentuální bonus k poškození proti PVP (předměty)"), default=0, blank=True, null=True)
    poskozeni_schopnosti_procenta_it_bonus = models.FloatField(("Procentuální bonus k poškození ze schopností (předměty)"), default=0, blank=True, null=True)
    poskozeni_utokem_procenta_it_bonus = models.FloatField(("Procentuální bonus k poškození z útoku (předměty)"), default=0, blank=True, null=True)
    sance_na_otravu_procenta_it_bonus = models.FloatField(("Procentuální šance na otravu (předměty)"), default=0, blank=True, null=True)
    sance_na_bezvedomi_procenta_it_bonus = models.FloatField(("Procentuální šance na bezvědomí (předměty)"), default=0, blank=True, null=True)
    kriticke_poskozeni_procenta_it_bonus = models.FloatField(("Procentuální bonus ke kritickému poškození (předměty)"), default=0, blank=True, null=True)

    price = models.IntegerField(default=0)
    sell_price = models.FloatField(("Prodejní cena"), default=0)

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
        # Nejprve ulož samotný předmět
        super().save(*args, **kwargs)


        if self.hrac:
            char_bonus, created = Character_bonus.objects.get_or_create(hrac=self.hrac)
            char_bonus.save()  # tím se přepočítají bonusy podle všech EQP

            # --- přepočítání Atributs ---
            atributy, created = Atributs.objects.get_or_create(hrac=self.hrac)
            atributy.save()

    def __str__(self):
        return f"{self.name} ({self.hrac})"
    

class fight_log(models.Model):
    hrac = models.ForeignKey(Playerinfo, on_delete=models.CASCADE, related_name='fight_log', blank=True)
    mob_ID = models.IntegerField(blank=True, null=True)
    
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        # Po uložení nového záznamu zkontroluj počet záznamů a smaž staré, pokud je jich více než 50
        logs = fight_log.objects.filter(hrac=self.hrac).order_by('-created_at')