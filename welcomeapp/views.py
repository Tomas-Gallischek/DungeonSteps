from re import S
from django.shortcuts import render
from django.shortcuts import redirect, render
from django.shortcuts import render, redirect
from .rasy_povolani import rasa_povolani_bonus_create
from hracapp.models import EQP, INV, XP_LVL, Atributs, Character_bonus, Economy, ShopOffer, XP_Log
from .forms import RegistrationForm
from django.contrib.auth import login



def index(request):
    return render(request, 'welcomeapp/index.html')

def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()

            XP_LVL.objects.create(hrac=user)
            XP_Log.objects.create(hrac=user)
            Economy.objects.create(hrac=user)
            Atributs.objects.create(hrac=user)
            Character_bonus.objects.create(hrac=user)
            ShopOffer.objects.create(hrac=user)
            INV.objects.create(hrac=user)
            EQP.objects.create(hrac=user)
            
            login(request, user)
            rasa_povolani_bonus_create(request) # <-- Naštení základních hodnota atributů
            print(f"Uživatel {user.username} byl úspěšně zaregistrován a přihlášen.")

            return redirect('profile-url')
    else:
        form = RegistrationForm()
    return render(request, 'welcomeapp/register.html', {'form': form})
