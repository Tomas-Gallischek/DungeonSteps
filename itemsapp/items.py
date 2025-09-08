import os
from urllib import request
import django
import sys
import random

GREEN = '\033[92m'
RED = '\033[91m'
RESET = '\033[0m'

def items_generator(request):

    

    return {

    }







#   PRO SPUŠTĚNÍ SKRIPTU 
if __name__ == "__main__": # <-- KÓD PRO SPRÁVNÉ SPUŠTĚNÍ PŘI TESTOVÁNÍ FUNKCE + IMPORT DATABÁZE
    # Nastavení Django prostředí
    # Zde se ujistíte, že je správná cesta k projektu na Python path
    current_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(current_dir)
    sys.path.append(project_root)

    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'houska.settings')
    django.setup()
    
    # Import modelu se nyní provádí až po nastavení Django prostředí
    from hracapp.models import Playerinfo
    from itemsapp.models import Items
    # Spuštění testu s konkrétním uživatelem
    user = Playerinfo.objects.get(username='Shrek')
    result = items_generator(user)