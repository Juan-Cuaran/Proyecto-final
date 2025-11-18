from django import forms
from .models import CredentialsModel


class CredentialsForm(forms.ModelForm):
    class Meta:
        model = CredentialsModel
        fields = ['expiration_date', 'restricted', 'active']
        widgets = {
            'expiration_date': forms.DateTimeInput(attrs={'class': 'input-field', 'type': 'datetime-local'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if 'credential_code' in self.fields:
            self.fields.pop('credential_code')
        if 'visitor' in self.fields:
            self.fields.pop('visitor')