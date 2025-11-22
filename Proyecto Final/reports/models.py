from django.db import models
from django.utils import timezone


class Report(models.Model):
    FILTER_CHOICES = [
        ('HORA', 'Hora'),
        ('ESTADO', 'Estado de acceso'),
    ]

    filter_by = models.CharField(max_length=10, choices=FILTER_CHOICES)
    hour_from = models.TimeField(null=True, blank=True)
    hour_to = models.TimeField(null=True, blank=True)
    estado_acceso = models.CharField(max_length=5, null=True, blank=True)
    generated_at = models.DateTimeField(default=timezone.now)
    events = models.ManyToManyField('accesscontrol.AccessEventModels', related_name='reports')
    total_events = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"Reporte {self.id} - {self.get_filter_by_display()} ({self.generated_at:%Y-%m-%d %H:%M})"
