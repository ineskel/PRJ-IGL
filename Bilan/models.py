from django.db import models
from django.contrib.auth import get_user_model
from Consultation.models import Consultation
# Create your models here. il peut prescrire des examens complémentaires en lui rédigeant un bilan biologique et/ou radiologique
class BilanBiologique(models.Model):
    IdBilanBiologique = models.AutoField(primary_key=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    parametre = models.CharField(max_length=25)
    valeur = models.FloatField()
    laborantin = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, limit_choices_to={'role': 'laborantin'},null=True,related_name='BilanBiologique_Laborantin')
    Consultation = models.ForeignKey('Consultation.Consultation', on_delete=models.CASCADE, related_name='BilanBiologique_Consultation')
    def __str__(self):
        return f"Bilan Biologique cree par {self.Medecin} pour le patient {self.DPI}"
    
class BilanRadiologique(models.Model):
    IdBilanRadiologique = models.AutoField(primary_key=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    examen = models.CharField(max_length=25)
    image = models.URLField()
    compterendu = models.TextField()
    radiologue = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, limit_choices_to={'role': 'radiologue'},null=True,related_name='BilanRadiologique_Radiologue')
    Consultation = models.ForeignKey('Consultation.Consultation', on_delete=models.CASCADE, related_name='BilanRadiologique_Consultation')
    def __str__(self):
        return f"Bilan Radiologique cree par {self.Medecin} pour le patient {self.DPI}"
 

class DemandeBilan(models.Model):
    IdDemandeBilan = models.AutoField(primary_key=True)
    created_at = models.DateTimeField(auto_now_add=True)
    patient = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, limit_choices_to={'role': 'patient'},null=True,related_name='DemandeBilan_patient')
    Consultation = models.ForeignKey('Consultation.Consultation', on_delete=models.CASCADE, related_name='Demande_Consultation',null=True)
    BILAN_CHOICES = (
        ('B', 'Biologique'),
        ('R', 'Radiologique'),
    )
    typebilan = models.CharField(max_length=1, choices=BILAN_CHOICES)
    TypeTest = models.CharField(max_length=150)
    DEMANDE_ETATS= (
        ('enattente', 'En attente'),
        ('traitee', 'Traitée'),
    )
    etat = models.CharField(max_length=10, choices=DEMANDE_ETATS, default='enattente')
    def __str__(self):
        return f"Demande de Bilan pour le patient {self.IdDemandeBilan}"
    
