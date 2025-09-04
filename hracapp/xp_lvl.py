from django.shortcuts import redirect
from .models import XP_LVL, XP_Log

def plus_xp(request):
    user = request.user
    xp_model = XP_LVL.objects.get(hrac=user)
    new_xp = request.POST.get('new_xp', 0)
    xp_model.xp += int(new_xp)

    # Create a new XP_Log entry
    xp_log = XP_Log(hrac=user)
    xp_log.xp_record = int(new_xp)
    xp_log.save()
    xp_model.save()

    return redirect('profile-url')
