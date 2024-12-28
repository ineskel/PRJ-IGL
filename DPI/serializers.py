from rest_framework import serializers
from .models import DPI
from Consultation.serializers import ConsultationCreateSerializer
from Soins.serializers import SoinsCreateSerializer


class DPISerializer(serializers.ModelSerializer):
    class Meta:
        model = DPI
        fields = ['NSS', 'Nom', 'Prenom', 'DateDeNaissonce', 'Adress', 'Numero', 'Mutuelle', 'sexe', 'ContactNom', 'ContactNumero', 'created_at', 'updated_at', 'Patient']
        
        
class DPIDetailSerializer(serializers.ModelSerializer):
    soins= SoinsCreateSerializer(many=True,allow_null=True)
    consultations = ConsultationCreateSerializer(many=True,allow_null=True)
    class Meta:
        model = DPI
        fields = ['NSS', 'Nom', 'Prenom', 'DateDeNaissonce', 'Adress', 'Numero', 'Mutuelle', 'sexe', 'ContactNom', 'ContactNumero', 'created_at', 'updated_at', 'soins', 'consultations']