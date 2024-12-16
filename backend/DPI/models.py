from django.db import models

# Create your models here.
from django.db import models

class DPI(models.Model):
    NSS = models.BigIntegerField(unique=True)
    Nom = models.CharField(max_length=20)
    Prenom = models.CharField(max_length=20)
    DateDeNaissonce = models.DateField()
    Adress = models.CharField(max_length=45)
    Numero = models.CharField(max_length=20)
    Mutuelle = models.CharField(max_length=45, null=True, blank=True)
    SEX_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
    ]
    sexe = models.CharField(max_length=1, choices=SEX_CHOICES)
    ContactNom = models.CharField(max_length=20)
    ContactNumero = models.CharField(max_length=20)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    def __str__(self):
        return f"{self.Nom} {self.Prenom}"

class Patient(models.Model):
    DPI_NSS = models.OneToOneField(DPI, on_delete=models.CASCADE, to_field="NSS")
    email = models.EmailField(unique=True)
    Password = models.CharField(max_length=20)
    def __str__(self):
        return f"Patient {self.DPI_NSS.Nom}"
