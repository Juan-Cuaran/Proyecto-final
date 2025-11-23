from django.shortcuts import render, redirect
from django.contrib import messages
from datetime import datetime
from .models import AccessEventModels, AccessPoint
from .forms import accescontrolform
from credentials.models import CredentialsModel
from reports.models import Report

FILTROS_REPORTES = (
    ('HORA', 'Horas de acceso'),
    ('ESTADO', 'Estados de acceso'),
)

ESTADOS_ACCESO = (
    ('ENTRY', 'Entrada'),
    ('EXIT', 'Salida'),
)


def create_access_event(request):
    context = {}

    if request.method == 'POST':
        access_point_name = request.POST.get('access_point', '').strip()
        credential_code = request.POST.get('credential_code', '').strip()
        status = request.POST.get('status', '')

        if not access_point_name or not credential_code or not status:
            messages.error(request, 'Todos los campos son obligatorios.')
            return render(request, 'accesscontrol/create_access_event.html', context)

        access_point, created = AccessPoint.objects.get_or_create(name=access_point_name)

        credential = None
        code_raw = credential_code
        try:
            credential = CredentialsModel.objects.get(credential_code=code_raw)
        except CredentialsModel.DoesNotExist:
            digits = ''.join(ch for ch in code_raw if ch.isdigit())
            if digits:
                try:
                    credential = CredentialsModel.objects.get(credential_code=digits)
                except CredentialsModel.DoesNotExist:
                    try:
                        credential = CredentialsModel.objects.get(credential_code=digits.zfill(6))
                    except CredentialsModel.DoesNotExist:
                        credential = None
            if not credential:
                qs = CredentialsModel.objects.filter(visitor__name__icontains=code_raw)
                if qs.exists():
                    credential = qs.first()

        if not credential:
            messages.error(request, f'No se encontró la credencial con código o visitante: "{credential_code}"')
            return render(request, 'accesscontrol/create_access_event.html', context)

        messages.success(request, f'Credencial encontrada: {credential.credential_code} (id={credential.id})')

        access_event = AccessEventModels(
            access_point=access_point,
            credential=credential,
            status=status
        )
        access_event.save()

        messages.success(request, 'Evento de acceso registrado exitosamente.')
        return redirect('dashboard')

    return render(request, 'accesscontrol/create_access_event.html', context)


def create_reports(request):
    context = {
        'filtros_reportes': FILTROS_REPORTES,
        'estados_acceso': ESTADOS_ACCESO,
    }
    database = None
    message = None

    filter_by = (request.POST.get('filter_by') or '').strip().upper()
    estado = (request.POST.get('estado_acceso') or '').strip().upper()
    context['selected_filter'] = filter_by
    context['selected_estado'] = estado

    if request.method == 'POST':
        hour_from = (request.POST.get('hour_from') or '').strip()
        hour_to = (request.POST.get('hour_to') or '').strip()

        if not AccessEventModels.objects.exists():
            message = 'No hay eventos registrados para generar el reporte.'
        else:
            if filter_by not in dict(FILTROS_REPORTES):
                message = 'Seleccione un filtro válido.'
            else:
                qs = AccessEventModels.objects.select_related('credential', 'access_point').all()

                if filter_by == 'HORA':
                    if not hour_from and not hour_to:
                        message = 'Ingrese al menos una hora inicial o final.'
                    else:
                        if hour_from:
                            qs = qs.filter(timestamp__time__gte=hour_from)
                        if hour_to:
                            qs = qs.filter(timestamp__time__lte=hour_to)
                        database = qs

                elif filter_by == 'ESTADO':
                    if estado not in dict(ESTADOS_ACCESO):
                        message = 'Seleccione Entrada o Salida.'
                    else:
                        qs = qs.filter(status__iexact=estado)
                        database = qs

        if database is not None and not database.exists():
            message = 'No se encontraron eventos con ese criterio.'
            database = None

    if message:
        context['message'] = message
    if database is not None:
        database = database.order_by('-timestamp')
        context['database'] = database
        # Guardar reporte generado
        hour_from = request.POST.get('hour_from') or None
        hour_to = request.POST.get('hour_to') or None

        def parse_time(val):
            try:
                return datetime.strptime(val, '%H:%M').time()
            except (TypeError, ValueError):
                return None

        report = Report.objects.create(
            filter_by=filter_by,
            hour_from=parse_time(hour_from) if filter_by == 'HORA' else None,
            hour_to=parse_time(hour_to) if filter_by == 'HORA' else None,
            estado_acceso=estado if filter_by == 'ESTADO' else None,
            total_events=database.count()
        )
        report.events.set(database)
        context['report_saved'] = True

    return render(request, 'accesscontrol/reports.html', context)
