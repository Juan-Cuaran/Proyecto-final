from django.shortcuts import render, get_list_or_404, redirect
from django.urls import reverse
from django.db.models import OuterRef, Subquery
from .models import Visitor
from .form import VisitorForm
from credentials.models import CredentialsModel


# Create your views here.

def create_visitor(request):
    context = {}
    form = VisitorForm(request.POST or None)
    if form.is_valid():
        visitor = form.save()
        context['message'] = 'Visitante registrado exitosamente.'
        return redirect(f"{reverse('create_credential')}?visitor_id={visitor.id}")
    context['form'] = form
    return render(request, 'create_visitor.html', context)

def list_visitor(request):
    context = {}
    visitors = None
    message = None

    selected_id = request.GET.get('id')
    if selected_id:
        latest_cred = CredentialsModel.objects.filter(visitor=OuterRef('pk')).order_by('-issued_at')
        visitors = Visitor.objects.filter(id_visitor__exact=selected_id).annotate(
            credential_code=Subquery(latest_cred.values('credential_code')[:1]),
            credential_active=Subquery(latest_cred.values('active')[:1]),
        )
        if not visitors.exists():
            message = 'No se encontraron visitantes con ese ID.'
        context['visitors'] = visitors
        context['message'] = message
        return render(request, 'list_visitors.html', context)

    if request.method == 'POST':
        search_by = request.POST.get('search_by')
        q = request.POST.get('q', '').strip()
        if not q:
            message = 'Introduzca un término de búsqueda.'
        else:
            base_query = Visitor.objects.all()
            if search_by == 'id':
                base_query = base_query.filter(id_visitor__exact=q)
            else:
                base_query = base_query.filter(name__icontains=q)

            latest_cred = CredentialsModel.objects.filter(visitor=OuterRef('pk')).order_by('-issued_at')
            visitors = base_query.annotate(
                credential_code=Subquery(latest_cred.values('credential_code')[:1]),
                credential_active=Subquery(latest_cred.values('active')[:1]),
            )
            if not visitors.exists():
                message = 'No se encontraron coincidencias.'

    context['visitors'] = visitors
    context['message'] = message
    return render(request, 'list_visitors.html', context)

def restrict_visitor(request):
    context = {}
    if request.method == 'POST':
        idv = request.POST.get('id_visitor', '').strip()
        motive = request.POST.get('motive', '').strip()
        if not idv or not motive:
            context['message'] = 'Ingrese ID de visitante y motivo.'
        else:
            try:
                visitor = Visitor.objects.get(id_visitor=idv)
                visitor.motive = motive
                visitor.save()
                context['message'] = f"Motivo guardado para visitante {visitor.name}."
                context['visitor'] = visitor
            except Visitor.DoesNotExist:
                context['message'] = 'No se encontró visitante con ese ID.'

    return render(request, 'restrict_visitor.html', context)
