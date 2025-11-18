from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from .models import CredentialsModel
from visitors.models import Visitor
from datetime import timedelta
from django.utils import timezone
import random

def Asign_credential(request):
    context = {}
    visitor_id = request.GET.get('visitor_id') or request.POST.get('visitor_id')
    visitor = None
    if visitor_id:
        visitor = get_object_or_404(Visitor, pk=visitor_id)

    expiration_days = {
        'TEMP': 2,
        'PROV': 10,
        'EMP': 20,
    }
    if request.method == 'POST':
        if not visitor:
            messages.error(request, 'Visitante no especificado.')
            return redirect('list_visitor')

        cred = CredentialsModel(visitor=visitor)
        days = expiration_days.get(visitor.visitor_type, 2)
        cred.expiration_date = timezone.now() + timedelta(days=days)
        cred.save()
        messages.success(request, 'Credencial digital generada correctamente!')
        return redirect('list_visitor')

    preview = None
    for _ in range(10):
        candidate = str(random.randint(0, 999999)).zfill(6)
        if not CredentialsModel.objects.filter(credential_code=candidate).exists():
            preview = candidate
            break
    context['form'] = None
    context['visitor'] = visitor
    context['preview_code'] = preview
    return render(request, 'credentials/create_credential.html', context)

   