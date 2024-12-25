from rest_framework import serializers
from .models import DPI


class DPISerializer(serializers.ModelSerializer):
    class Meta:
        model = DPI
        fields = ['NSS', 'Nom', 'Prenom', 'DateDeNaissonce', 'Adress', 'Numero', 'Mutuelle', 'sexe', 'ContactNom', 'ContactNumero', 'created_at', 'updated_at', 'Patient']
        
        
