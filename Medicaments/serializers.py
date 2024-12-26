from rest_framework import serializers
from .models import Medicament , MedicamentOrdonnance
from Ordonnance.models import Ordonnance
class MedicamentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Medicament
        fields = '__all__'
        
class MedicamentOrdonnanceSerializer(serializers.ModelSerializer):
    ordonnance = serializers.PrimaryKeyRelatedField(queryset=Ordonnance.objects.all())
    medicament = serializers.PrimaryKeyRelatedField(queryset=Medicament.objects.all())
    class Meta:
        model = MedicamentOrdonnance
        fields = ['IdMedicamentOrdonnance', 'Medicament', 'Ordonnance', 'dose', 'duree']
        
        
class MedicamentOrdonnanceCreateSerializer(serializers.ModelSerializer):
    Medicament = MedicamentSerializer()
    class Meta:
        model = MedicamentOrdonnance
        fields = ['IdMedicamentOrdonnance', 'Medicament', 'dose', 'duree']
                       
class OrdonnanceSerializer(serializers.ModelSerializer):
    medicaments = MedicamentOrdonnanceCreateSerializer(many=True, source='ordonnance')
    class Meta:
        model = Ordonnance
        fields = ['IdOrdonnance',  'statue', 'medicaments']