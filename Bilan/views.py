from rest_framework import status
from rest_framework.response import Response
from Compte.permissions import IsLaborantin , IsRadiologue , IsMedecin
from .serializers import BilanBiologiqueSerializer, BilanRadiologiqueSerializer , DemandeBilanSerializer
from rest_framework.decorators import api_view, permission_classes
# create BilanBiolgique 
@api_view(['POST'])
@permission_classes([IsLaborantin])
def create_bilanbiologique(request, pk):
    laborantin = request.user
    data = request.data
    data['laborantin'] = laborantin.id
    data['Consultation'] = pk
    # Create the BilanBiologique instance
    serializer = BilanBiologiqueSerializer(data=data)
    if serializer.is_valid():
        # Save the BilanBiologique
        serializer.save()        
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
# create BilanRadiologique with try except
@api_view(['POST'])
@permission_classes([IsRadiologue])
def create_bilanradiologique(request, pk):
    radiologue = request.user
    data = request.data
    data['radiologue'] = radiologue.id
    data['Consultation'] = pk
    # Create the BilanRadiologique instance
    serializer = BilanRadiologiqueSerializer(data=data)
    if serializer.is_valid():
        # Save the BilanRadiologique
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)