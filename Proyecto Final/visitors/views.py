from django.shortcuts import render,get_list_or_404
from .models import Visitor
from .form import VisitorForm


# Create your views here.

def create_visitor(request):
    context = {}
    form = VisitorForm(request.POST or None)
    if form.is_valid():
        form.save()
        context['message'] = 'Visitante registrado exitosamente.'
    context['form'] = form
    return render(request, 'create_visitor.html', context)

def list_visitor(request):
    context = {}
    visitors = None
    message = None

    selected_id = request.GET.get('id')
    if selected_id:
        visitors = Visitor.objects.filter(id_visitor__exact=selected_id)
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
            if search_by == 'id':
                visitors = Visitor.objects.filter(id_visitor__exact=q)
            else:
                visitors = Visitor.objects.filter(name__icontains=q)
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
