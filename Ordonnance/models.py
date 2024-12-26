from django.db import models
from Consultation.models import Consultation
# Create your models here.
class Ordonnance(models.Model):
    IdOrdonnance = models.AutoField(primary_key=True)
    created_at = models.DateTimeField(auto_now_add=True)
    STATUE = (
        ('V', 'Validee'),
        ('NV', 'Non Validee'),
        ('A', 'Attente'),
    )
    statue = models.CharField(max_length=2, choices=STATUE, default='A')
    consultation = models.ForeignKey(Consultation, on_delete=models.CASCADE, related_name='consultation_ordonnance')
    def __str__(self):
        return f"{self.IdOrdonnance}"