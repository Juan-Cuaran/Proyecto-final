from django.shortcuts import render, redirect
from .models import AccessEventModels
from .forms import accescontrolform
from django.contrib import messages
from credentials.models import CredentialsModel
# Create your views here.

def create_access_event(request):
    context ={}
    # accept credential identifier as either the DB id or the 6-digit code
    credential_id = request.GET.get('credential_id') or request.POST.get('credential_id')
    credential_code = request.GET.get('credential_code') or request.POST.get('credential_code')
    credencial = None
    if credential_id:
        credencial = CredentialsModel.objects.filter(id=credential_id).first()
    elif credential_code:
        credencial = CredentialsModel.objects.filter(credential_code=credential_code).first()

    
    if request.method == 'POST':
        form = accescontrolform(request.POST)
        if form.is_valid():
            access_event = form.save(commit=False)
            if credencial:
                access_event.credential = credencial
            access_event.save()
            messages.success(request, 'Evento de acceso registrado exitosamente.')
            return redirect('list_access_events')
        if not credencial:
            messages.error(request, 'No se ha encontrado la credencial digitada.')

        context['form'] = form
        context['credential'] = credencial
        return render(request, 'accesscontrol/create_access_event.html', context)

    form = accescontrolform()
    context['form'] = form
    context['credential'] = credencial
    return render(request, 'accesscontrol/create_access_event.html', context)

def list_access_events(request):
    context = {}
    context['database'] = AccessEventModels.objects.all()    
    return render(request, 'accesscontrol/list_access_events.html', context)