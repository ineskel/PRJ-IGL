from django.db import models
from django.contrib.auth import get_user_model
from Consultation.models import Consultation
# Create your models here.
class DPI(models.Model):
    # nss is a primary key and it's unique
    idDPI = models.AutoField(primary_key=True)
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
    Patient = models.OneToOneField(get_user_model(), on_delete=models.CASCADE, limit_choices_to={'role': 'patient'},related_name='DPI_Patient')
    def __str__(self):
        return f"{self.Nom} {self.Prenom}"
    