from django.db import models

# Create your models here.
# Clases Tablas SQL

class UsersModel (models.Model):
    Name = models.CharField(max_length=100)
    UsersID = models.CharField(max_length=10, unique=True)
    Password = models.CharField(max_length=10)
    ROLE_CHOICES = [
        ("admin", "Administrador"),
        ("vigilante", "Vigilante"),
    ]
    Role = models.CharField(max_length=10, choices=ROLE_CHOICES, default="vigilante")



