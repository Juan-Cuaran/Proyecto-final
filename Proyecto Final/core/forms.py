from django import forms
from models import UsersModel

class UserForms(forms.ModelForm):

    class meta:
        
        model = UsersModel()
        fields = ['Name', 'UsersID', 'Password']
        labels = {'Name': 'Nombre del usuario', 
                  'UsersID': 'Id del usuario',
                  'password': 'Contraseña'
                  }
        
        widgets ={
            'Name':forms.TextInput(attrs={'class': 'CSS_CLASS'}),
            'UsersID':forms.TextInput(attrs={'class': 'CSS_CLASS'}),
            'Password':forms.TextInput(attrs={'class': 'CSS_CLASS'})
        }