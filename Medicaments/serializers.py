from rest_framework import serializers
from .models import Medicament, MedicamentOrdonnance, Ordonnance

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
    medicaments = MedicamentOrdonnanceCreateSerializer(many=True, source='ordonnance_medicament')
    class Meta:
        model = Ordonnance
        fields = ['IdOrdonnance', 'medicaments' , 'consultation']
        
        
    def create(self, validated_data):
        try:
            # Extract medicaments data from validated_data
            medicaments_data = validated_data.pop('ordonnance_medicament')
            
            # Create the Ordonnance instance
            ordonnance = Ordonnance.objects.create(**validated_data)
            
            # Create each MedicamentOrdonnance instance
            for medicament_data in medicaments_data:
                medicament_info = medicament_data.pop('Medicament')
                # Get or create the Medicament instance
                medicament, _ = Medicament.objects.get_or_create(**medicament_info)
                
                # Create the MedicamentOrdonnance with the relationship
                MedicamentOrdonnance.objects.create(
                    Ordonnance=ordonnance,
                    Medicament=medicament,
                    **medicament_data
                )
            
            # Refresh from database to ensure we have all related data
            ordonnance.refresh_from_db()
            return ordonnance
            
        except Exception as e:
            raise serializers.ValidationError(f"Failed to create ordonnance: {str(e)}")