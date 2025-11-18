from django import forms
from .models import Visitor

class VisitorForm(forms.ModelForm):
    class Meta:
        model = Visitor
        fields = ['name', 'id_visitor', 'visitor_type', 'motive']
        labels = {
            'name': 'Nombre del visitante',
            'id_visitor': 'ID del visitante',
            'visitor_type': 'Tipo de visitante',
            'motive': 'Motivo de la visita',
        }
        widgets = {
            'name': forms.TextInput(attrs={'class': 'input-field'}),
            'id_visitor': forms.TextInput(attrs={'class': 'input-field'}),
            'visitor_type': forms.Select(attrs={'class': 'input-field'}),
            'motive': forms.TextInput(attrs={'class': 'input-field'}),
        }