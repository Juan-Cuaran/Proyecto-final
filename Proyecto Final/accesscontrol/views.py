from django.shortcuts import render, redirect
from .models import AccessEventModels, AccessPoint
from .forms import accescontrolform
from django.contrib import messages
from credentials.models import CredentialsModel
# Create your views here.

def create_access_event(request):
    context = {}
    
    if request.method == 'POST':
        # Obtener los datos del formulario
        access_point_name = request.POST.get('access_point', '').strip()
        credential_code = request.POST.get('credential_code', '').strip()
        status = request.POST.get('status', '')
        
        # Validar que todos los campos estén presentes
        if not access_point_name or not credential_code or not status:
            messages.error(request, 'Todos los campos son obligatorios.')
            return render(request, 'accesscontrol/create_access_event.html', context)
        
        # Buscar o crear el punto de acceso
        access_point, created = AccessPoint.objects.get_or_create(name=access_point_name)
        
        # Buscar la credencial
        try:
            credential = CredentialsModel.objects.get(credential_code=credential_code)
        except CredentialsModel.DoesNotExist:
            messages.error(request, f'No se encontró la credencial con código: {credential_code}')
            return render(request, 'accesscontrol/create_access_event.html', context)
        
        # Crear el evento de acceso
        access_event = AccessEventModels(
            access_point=access_point,
            credential=credential,
            status=status
        )
        access_event.save()
        
        messages.success(request, 'Evento de acceso registrado exitosamente.')
        return redirect('list_access_events')
    
    return render(request, 'accesscontrol/create_access_event.html', context)

def list_access_events(request):
    context = {}
    context['database'] = AccessEventModels.objects.all()    
    return render(request, 'accesscontrol/list_access_events.html', context)