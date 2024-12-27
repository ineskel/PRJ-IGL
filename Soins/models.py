from django.db import models
from DPI.models import DPI
from django.contrib.auth import get_user_model

# Create your models here.
class Soin(models.Model):
    IdSoin = models.AutoField(primary_key=True)
    created_at = models.DateTimeField(auto_now_add=True)
    soins = models.CharField(max_length=255)
    observations = models.TextField(blank=True, null=True, default='')
    DPI = models.ForeignKey(DPI, on_delete=models.CASCADE, related_name='DPI_Soin')
    infermier = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, limit_choices_to={'role': 'infermier'},related_name='Soin_infermier')
    def __str__(self):
        return f"{self.IdSoin}"