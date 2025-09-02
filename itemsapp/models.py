from django.db import models

class Weapons(models.Model):

    TYPE_CHOICES = (
        ('none', 'Žádná'),
        ('heavy', 'Těžké'),
        ('light', 'Lehké'),
        ('magic', 'Magické'),
    )

    img_init = models.CharField(max_length=100, default='', blank=True, null=True)
    name = models.CharField(max_length=100, default='', blank=True, null=True)
    type = models.CharField(max_length=10, choices=TYPE_CHOICES, default='none')
    level_required = models.IntegerField(default=1)
    level_stop = models.IntegerField(default=10)
    description = models.TextField(max_length=500, default='', blank=True, null=True)

    def __str__(self):
        return self.name