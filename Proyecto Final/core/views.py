from django.shortcuts import render, get_list_or_404
from django.http import HttpResponse, JsonResponse
from .models import UsersModel
# Create your views here.
#HTML

def create_view (request):
    context = {}
    form = UsersModel(request.POST or None)
    if form.is_valid 