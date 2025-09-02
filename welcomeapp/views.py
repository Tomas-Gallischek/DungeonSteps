from django.shortcuts import render
import json
from django.contrib.auth import logout
from django.shortcuts import redirect, render
from django.views.decorators.csrf import csrf_protect
from django.shortcuts import render, redirect

from hracapp.models import Atributs
from .forms import RegistrationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login


def index(request):
    return render(request, 'welcomeapp/index.html')

def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()

            # Tady vytvoř záznam Atributs pro nového uživatele
            Atributs.objects.create(hrac=user)

            # Až teď přihlas uživatele
            login(request, user)
            return redirect('profile-url')
    else:
        form = RegistrationForm()
    return render(request, 'welcomeapp/register.html', {'form': form})
