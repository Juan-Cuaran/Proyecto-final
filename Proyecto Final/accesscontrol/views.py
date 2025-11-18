from django.shortcuts import render, redirect
from .models import AccessEventModels, AccessPoint
from .forms import accescontrolform
from django.contrib import messages
from credentials.models import CredentialsModel
import re
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

        # Buscar la credencial: varios intentos de normalización para evitar fallos por espacios,
        # ceros a la izquierda faltantes o búsquedas por nombre de visitante.
        credential = None
        code_raw = credential_code
        # 1) intento directo
        try:
            credential = CredentialsModel.objects.get(credential_code=code_raw)
        except CredentialsModel.DoesNotExist:
            # 2) intentar sólo los dígitos (quitar espacios/caracteres no numéricos)
            digits = ''.join(ch for ch in code_raw if ch.isdigit())
            if digits:
                try:
                    credential = CredentialsModel.objects.get(credential_code=digits)
                except CredentialsModel.DoesNotExist:
                    # 3) intentar rellenar a 6 dígitos (si las credenciales tienen 6 dígitos)
                    try:
                        credential = CredentialsModel.objects.get(credential_code=digits.zfill(6))
                    except CredentialsModel.DoesNotExist:
                        credential = None
            # 4) si no es numérico o aún no encontrado, intentar buscar por nombre de visitante
            if not credential:
                qs = CredentialsModel.objects.filter(visitor__name__icontains=code_raw)
                if qs.exists():
                    credential = qs.first()

        if not credential:
            messages.error(request, f'No se encontró la credencial con código o visitante: "{credential_code}"')
            return render(request, 'accesscontrol/create_access_event.html', context)
        # Informar cuál credencial se usará (útil para depuración en la UI y en logs)
        messages.success(request, f'Credencial encontrada: {credential.credential_code} (id={credential.id})')
        print(f"[accesscontrol] matched credential: id={credential.id} code={credential.credential_code} for input '{credential_code}'")
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
    # usar select_related para reducir consultas y ordenar por fecha más reciente
    context['database'] = AccessEventModels.objects.select_related('credential', 'access_point').all().order_by('-timestamp')
    return render(request, 'accesscontrol/list_access_events.html', context)