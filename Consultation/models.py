from django.db import models
from django.contrib.auth import get_user_model
from DPI.models import DPI
# Create your models here.
class Consultation(models.Model):
    IdConsultation = models.AutoField(primary_key=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    resume = models.TextField(blank=True, null=True)
    medecin = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, limit_choices_to={'role': 'medecin'},related_name='Consultation_Medecin')
    DPI = models.ForeignKey(DPI, on_delete=models.CASCADE, related_name='Consultation_DPI')
    def __str__(self):
        return f"Consultation cree par DR {self.medecin.username} pour le patient {self.DPI}"
    