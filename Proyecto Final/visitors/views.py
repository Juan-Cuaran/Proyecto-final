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
    selected_id = request.GET.get('id')
    if selected_id:
        visitors = get_list_or_404(Visitor, id=selected_id)
        context['database'] = visitors
        return render(request, "list_view.html", context)
    matches = None
    message = None
    if request.method == 'POST':
        buscar_por = request.POST.get('search_by')
        q = request.POST.get('q', '').strip()
        if not q:
            message = 'Introduzca un término de búsqueda.'
        else:
            if buscar_por == 'id':
                matches = Visitor.objects.filter(id__exact=q)
            else:
                matches = Visitor.objects.filter(name__icontains=q)
            if not matches.exists():
                message = 'El parametro no se encuentra registrado en el sistema.'
    context['marches'] = matches
    context['message'] = message
    return render(request, "list_visitors.html", context)
