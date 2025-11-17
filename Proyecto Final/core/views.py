from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect, HttpRequest
from django.contrib import messages
from .models import UsersModel
from .forms import UserForms
# Create your views here.

def index(request):

    context = {}
    fallos = 0
    if request.method == 'POST' and request.POST.get('action') == 'login':
        uid = request.POST.get('UsersID', '').strip()
        pwd = request.POST.get('Password', '').strip()
        user_qs = UsersModel.objects.filter(UsersID=uid, Password=pwd)
        if user_qs.exists():
            user = user_qs.first()
            request.session['user_pk'] = user.pk
            request.session['user_name'] = user.Name
            request.session['user_role'] = user.Role
            return HttpResponseRedirect('/')    
        else:
            fallos += 1
            if fallos >= 3:
                context['login_error'] = 'Acceso invalido, inténtelo de nuevo en 5 minutos'
            context['login_error'] = 'Contraseña/ID inválidas.'

    if request.method == 'POST' and request.POST.get('action') == 'logout':
        for k in ('user_pk', 'user_name', 'user_role'):
            request.session.pop(k, None)
        return HttpResponseRedirect('/')

    context['user_name'] = request.session.get('user_name')
    context['user_role'] = request.session.get('user_role')
    return render(request, 'index.html', context)

def hello(request, username):
    return render(request, 'index.html', {'greet': username})

def menu(request):

    context = {}
    context['user_name'] = request.session.get('user_name')
    context['user_role'] = request.session.get('user_role')
    return render(request, 'menu.html', context)


def dashboard(request):

    context = {}
    userid = request.POST.get('UsersID', '').strip()
    userrole = request.POST.get('Role', '').strip()

    if not userid or not userrole:
        messages.error(request, 'Por favor, complete todos los campos obligatorios.')
        return render(request, 'index.html', {})
    
    elif userrole == 'admin':
        return HttpResponseRedirect('dashboardadmin/')
    
    elif userrole == 'vigilante':
        return HttpResponseRedirect('/dashboardvigilante/')
    
    context['user_name'] = request.session.get('user_name')
    context['user_role'] = request.session.get('user_role')

    return render(request, 'dashboard.html', context)

def create_view (request):
    context = {}
    form = UserForms(request.POST or None)
    if form.is_valid():
        form.save()
        return HttpResponseRedirect("/")

    context = {"form":form}    
    return render(request, "create_view.HTML", context)

def list_view (request):
    context = {}
    context['database'] = UsersModel.objects.all()
    return render(request, "list_view.html", context)

def update_view(request, id=None):
    context = {}
    selected_id = id or request.GET.get('id')
    if selected_id:
        obj = get_object_or_404(UsersModel, id=selected_id)
        form = UserForms(request.POST or None, instance=obj)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect("/")
        context['form'] = form
        context['object'] = obj
        return render(request, "Update_View.html", context)
    matches = None
    message = None
    if request.method == 'POST':
        search_by = request.POST.get('search_by')
        q = request.POST.get('q', '').strip()
        if not q:
            message = 'Introduzca un término de búsqueda.'
        else:
            if search_by == 'id':
                matches = UsersModel.objects.filter(id__exact=q)
            else:
                matches = UsersModel.objects.filter(Name__icontains=q)
            if not matches.exists():
                message = 'No se encontraron coincidencias.'

    context['matches'] = matches
    context['message'] = message
    return render(request, "Update_View.html", context)

def delete_view (request, id):

    context = {}
    obj = get_object_or_404(UsersModel, id=id)

    if request.method == "POST":
        obj.delete()
        return HttpResponseRedirect("/")
    
    context['object'] = obj
    return render(request, "Delete_viewUsers.html", context)