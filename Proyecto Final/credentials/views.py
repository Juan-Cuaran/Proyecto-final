from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from .models import CredentialsModel
from .forms import CredentialsForm
from visitors.models import Visitor


def Asign_credential(request):
    context = {}
    visitor_id = request.GET.get('visitor_id') or request.POST.get('visitor_id')
    visitor = None
    if visitor_id:
        visitor = get_object_or_404(Visitor, pk=visitor_id)

    if request.method == 'POST':
        form = CredentialsForm(request.POST)
        if form.is_valid():
            cred = form.save(commit=False)
            if visitor:
                cred.visitor = visitor
            cred.save()
            messages.success(request, 'Credencial digital generada correctamente!')
            return redirect('list_visitor')
    else:
        form = CredentialsForm()
    
    context['form'] = form
    context['visitor'] = visitor
    return render(request, 'credentials/create_credential.html', context)

   