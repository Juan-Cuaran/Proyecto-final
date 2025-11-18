from django.db import models
import random


class CredentialsModel(models.Model):
    credential_code = models.CharField(max_length=6, unique=True, editable=False, blank=True)
    visitor = models.ForeignKey('visitors.Visitor', on_delete=models.CASCADE)
    issued_at = models.DateTimeField(auto_now_add=True)
    restricted = models.BooleanField(default=False)
    active = models.BooleanField(default=True)
    expiration_date = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"Credencial {self.credential_code} - {self.visitor.name}"

    def _generate_code(self):
        return str(random.randint(0, 999999)).zfill(6)

    def save(self, *args, **kwargs):
        if not self.credential_code:
            code = self._generate_code()
            self.credential_code = code
        super().save(*args, **kwargs)

