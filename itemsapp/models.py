from turtle import mode
from django.db import models

class Items(models.Model):

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

    name = models.CharField(max_length=100, blank=True, null=True)
    item_id = models.CharField(max_length=100, unique=True)
    img_init = models.CharField(max_length=200, blank=True, null=True)
    description = models.TextField(max_length=500, blank=True, null=True)
    level_required = models.IntegerField(default=1, blank=True, null=True)
    level_stop = models.IntegerField(default=10, blank=True, null=True)
    item_type = models.CharField(max_length=20, choices=ITEM_TYPE_CHOICES, blank=True, null=True)
    item_category = models.CharField(max_length=20, choices=ITEM_CATEGORY_CHOICES, default=None)

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