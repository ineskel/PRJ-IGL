from django.db import models
from django.contrib.auth import get_user_model
from DPI.models import DPI
# Create your models here.
class Consultation(models.Model):
    # nss is a primary key and it's unique
    NSS = models.BigIntegerField(primary_key=True , unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    Medecin = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, limit_choices_to={'role': 'medecin'},related_name='Consultation_Medecin')
    DPI = models.ForeignKey(DPI, on_delete=models.CASCADE, related_name='Consultation_DPI')
    def __str__(self):
        return f"Consultation cree par {self.Medecin} pour le patient {self.DPI}"
    