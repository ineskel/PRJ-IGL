from rest_framework import serializers
from .models import Soin
from DPI.models import DPI
from django.contrib.auth import get_user_model

class SoinsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Soin
        fields = ['IdSoin', 'created_at', 'soins', 'observations', 'DPI', 'infermier']
        
        
class SoinsCreateSerializer(serializers.ModelSerializer):
    DPI = serializers.PrimaryKeyRelatedField(queryset=DPI.objects.all())
    infermier = serializers.PrimaryKeyRelatedField(queryset=get_user_model().objects.all())
    class Meta:
        model = Soin
        fields = ['IdSoin', 'soins', 'observations', 'DPI', 'infermier']