from rest_framework import serializers 
from .models import BilanBiologique,BilanRadiologique,DemandeBilan

class BilanBiologiqueSerializer(serializers.ModelSerializer):
    class Meta:
        model = BilanBiologique
        laborantin = serializers.StringRelatedField()
        fields = ['IdBilanBiologique', 'parametre', 'valeur', 'laborantin', 'Consultation']
        
class BilanRadiologiqueSerializer(serializers.ModelSerializer):
    class Meta:
        model = BilanRadiologique
        radiologue = serializers.StringRelatedField()
        fields = ['IdBilanRadiologique', 'examen', 'image','compterendu' , 'radiologue', 'Consultation']
        
class DemandeBilanSerializer(serializers.ModelSerializer):
    class Meta:
        model = DemandeBilan
        patient = serializers.StringRelatedField()
        fields = ['IdDemandeBilan', 'patient', 'typebilan', 'TypeTest']
        