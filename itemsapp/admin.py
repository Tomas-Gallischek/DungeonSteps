from django.contrib import admin

from .models import Items, Items_bonus
admin.site.site_header = "DungenSteps Admin"
admin.site.site_title = "DungenSteps Admin Portal"

admin.site.register(Items)
admin.site.register(Items_bonus)




