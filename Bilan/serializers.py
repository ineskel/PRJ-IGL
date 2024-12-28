from rest_framework import serializers 
from .models import BilanBiologique,BilanRadiologique,DemandeBilan


class BilanBiologiqueSerializer(serializers.ModelSerializer):
    class Meta:
        model = BilanBiologique
        fields = ['IdBilanBiologique', 'parametre', 'valeur', 'laborantin', 'Consultation']
     
class BilanRadiologiqueSerializer(serializers.ModelSerializer):
    class Meta:
        model = BilanRadiologique
        fields = ['IdBilanRadiologique', 'examen', 'image','compterendu' , 'radiologue', 'Consultation']
        
class DemandeBilanSerializer(serializers.ModelSerializer):
    class Meta:
        model = DemandeBilan
        fields = ['IdDemandeBilan', 'patient', 'typebilan', 'TypeTest']
        