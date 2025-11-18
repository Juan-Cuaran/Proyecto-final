from django.db import models
from django.utils import timezone

# Create your models here.
class AccessPoint(models.Model):
    name = models.CharField(max_length=80)

class AccessEventModels(models.Model):

    STATUS_ACCESS = [
        ('ENTRY', 'Entrada'),
        ('EXIT', 'Salida')
    ]

    timestamp = models.DateTimeField(default=timezone.now)
    access_point = models.ForeignKey(AccessPoint, on_delete=models.CASCADE)
    credential = models.ForeignKey('credentials.CredentialsModel',on_delete=models.SET_NULL, null=True, blank=True,
    related_name='access_events')
    status = models.CharField(max_length=5, choices=STATUS_ACCESS)

    def __str__(self):
        cred_code = self.credential.credential_code if self.credential else 'N/A'
        return f"{self.get_status_display()} at {self.access_point.name} ({cred_code})"
