from django import forms
from .models import UsersModel


class UserForms(forms.ModelForm):
    class Meta:
        model = UsersModel
        fields = ['Name', 'UsersID', 'Password', 'Role']
        labels = {
            'Name': 'Nombre del usuario',
            'UsersID': 'Id del usuario',
            'Password': 'Contraseña',
            'Role': 'Rol',
        }
        widgets = {
            'Name': forms.TextInput(attrs={'class': 'input-field'}),
            'UsersID': forms.TextInput(attrs={'class': 'input-field'}),
            'Password': forms.PasswordInput(attrs={'class': 'input-field'}),
            'Role': forms.Select(attrs={'class': 'input-field'}),
        }