from rest_framework import serializers
from .models import Consultation
from Bilan.serializers import BilanBiologiqueSerializer, BilanRadiologiqueSerializer
from Medicaments.serializers import OrdonnanceSerializer

class ConsultationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Consultation
        fields = '__all__'
        # resume is not required
        extra_kwargs = {'resume': {'required': False}}
        
class ConsultationCreateSerializer(serializers.ModelSerializer):
    ordonnance = OrdonnanceSerializer(many=True,required=False)
    bilanbiologique = BilanBiologiqueSerializer(many=True,required=False)
    bilanradiologique = BilanRadiologiqueSerializer(many=True,required=False)
    class Meta:
        model = Consultation
        fields = ['resume','DPI_id','ordonnance', 'bilanbiologique', 'bilanradiologique']
    