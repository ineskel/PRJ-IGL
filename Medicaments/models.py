from django.db import models
from Ordonnance.models import Ordonnance
from django.core.exceptions import ValidationError
# Create your models here.
class Medicament(models.Model):
    IdMedicament = models.AutoField(primary_key=True)
    nom = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    def __str__(self):
        return f"{self.nom}"
    
# class d association entre medicament et ordonnance
class MedicamentOrdonnance(models.Model):
    IdMedicamentOrdonnance = models.AutoField(primary_key=True)
    Medicament = models.ForeignKey(Medicament, on_delete=models.CASCADE, related_name='ordonnance')
    Ordonnance = models.ForeignKey(Ordonnance, on_delete=models.CASCADE, related_name='ordonnance')
    dose = models.FloatField()
    duree = models.IntegerField()
    def __str__(self):
        return f"{self.IdMedicament} {self.IdOrdonnance}"
    def clean(self):
        # Optional: Add validation
        if self.dose <= 0 :
            raise ValidationError("La dose doit être supérieure à 0")
        if self.duree <= 0:
            raise ValidationError("La durée doit être supérieure à 0")