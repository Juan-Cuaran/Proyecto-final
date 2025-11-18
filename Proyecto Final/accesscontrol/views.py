from django.shortcuts import render, redirect
from .models import AccessEventModels, AccessPoint
from .forms import accescontrolform
from django.contrib import messages
from credentials.models import CredentialsModel
# Create your views here.

def create_access_event(request):
    # prepare lookup for credential (accepts id or 6-digit code)
    credential_code = request.GET.get('credential_code') or request.POST.get('credential_code')
    credencial = None
    if credential_code:
        credential_code = credential_code.strip()
        credencial = CredentialsModel.objects.filter(credential_code=credential_code).first()

    # common context used for both GET and POST failure cases
    context = {'credential': credencial}

    if request.method == 'POST':
        form = accescontrolform(request.POST)
        if form.is_valid():
            access_event = form.save(commit=False)
            if credencial:
                access_event.credential = credencial
            access_event.save()
            messages.success(request, 'Evento de acceso registrado exitosamente.')
            return redirect('list_access_events')

        # fallback: template may submit free-text access_point and status
        access_point_name = request.POST.get('access_point')
        status = request.POST.get('status')
        if access_point_name and status:
            ap, _ = AccessPoint.objects.get_or_create(name=access_point_name)
            access_event = AccessEventModels(access_point=ap, status=status)
            if credencial:
                access_event.credential = credencial
            access_event.save()
            messages.success(request, 'Evento de acceso registrado.')
            return redirect('list_access_events')

        # if we reach here, the POST failed validation and no fallback applied
        if not credencial:
            messages.error(request, 'No se ha encontrado la credencial digitada.')
        context['form'] = form

        return render(request, 'accesscontrol/create_access_event.html', context)

    context['form'] = accescontrolform()
    context['credential'] = credencial
    print(credencial)
    return render(request, 'accesscontrol/create_access_event.html', context)

def list_access_events(request):
    context = {}
    context['database'] = AccessEventModels.objects.all()    
    return render(request, 'accesscontrol/list_access_events.html', context)