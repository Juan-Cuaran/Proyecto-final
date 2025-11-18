from django import forms
from accesscontrol.models import AccessEventModels

class accescontrolform (forms.ModelForm):
    class Meta:
        model = AccessEventModels
        fields = ['access_point', 'credential', 'status']
        labels = {
            'access_point': 'Punto de Acceso',
            'credential': 'Credencial',
            'status': 'Estado de Acceso',
        }
        widgets = {
            'access_point': forms.Select(attrs={'class': 'input-field'}),
            'credential': forms.Select(attrs={'class': 'input-field'}),
            'status': forms.Select(attrs={'class': 'input-field'}),
        }
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if 'timestamp' in self.fields:
            self.fields.pop('timestamp')
        if 'id' in self.fields:
            self.fields.pop('id')
            