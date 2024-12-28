from django.db import models
from Ordonnance.models import Ordonnance
from django.core.exceptions import ValidationError

class Medicament(models.Model):
    IdMedicament = models.AutoField(primary_key=True)
    nom = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    
    def __str__(self):
        return f"{self.nom}"
    
class MedicamentOrdonnance(models.Model):
    IdMedicamentOrdonnance = models.AutoField(primary_key=True)
    Medicament = models.ForeignKey(Medicament, on_delete=models.CASCADE, related_name='medicament_ordonnance')
    Ordonnance = models.ForeignKey(Ordonnance, on_delete=models.CASCADE, related_name='ordonnance_medicament')
    dose = models.FloatField()
    duree = models.IntegerField()
    
    def __str__(self):
        return f"{self.Medicament} {self.Ordonnance}"