from rest_framework import status 
from rest_framework.response import Response
from .models import Ordonnance
from Medicaments.serializers import OrdonnanceSerializer
from Compte.permissions import IsMedecin, IsPatient
from rest_framework.decorators import api_view, permission_classes

@api_view(['GET'])
@permission_classes([IsMedecin])
def Ordonnances(request):
        ordonnance = Ordonnance.objects.all()
        serializer = OrdonnanceSerializer(ordonnance, many=True)
        return Response(serializer.data)

@api_view(['GET'])
@permission_classes([IsMedecin])
def Ordonnanceid(request, pk):
        ordonnance = Ordonnance.objects.get(pk=pk)
        serializer = OrdonnanceSerializer(ordonnance)
        return Response(serializer.data)

@api_view(['POST'])
@permission_classes([IsMedecin])
def OrdonnanceAdd(request):
        serializer = OrdonnanceSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
# delete by id
@api_view(['DELETE'])
@permission_classes([IsMedecin])
def OrdonnanceDelete(request, pk):
        ordonnance = Ordonnance.objects.get(pk=pk)
        ordonnance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

# get the ordonnance that are not checked (status = A)
@api_view(['GET'])
@permission_classes([IsMedecin])
def OrdonnanceAttente(request):
        ordonnance = Ordonnance.objects.filter(statue='A')
        serializer = OrdonnanceSerializer(ordonnance, many=True)
        return Response(serializer.data)

# validate the ordonnance by id 
@api_view(['PUT'])
@permission_classes([IsMedecin])
def OrdonnanceValide(request):
        ordonnance = Ordonnance.objects.get(pk=pk)
        ordonnance.statue = 'V'
        ordonnance.save()
        serializer = OrdonnanceSerializer(ordonnance)
        return Response(serializer.data)
# unvalidate the ordonnance by id
@api_view(['PUT'])
@permission_classes([IsMedecin])
def OrdonnanceNonValide(request):
        ordonnance = Ordonnance.objects.get(pk=pk)
        ordonnance.statue = 'NV'
        ordonnance.save()
        serializer = OrdonnanceSerializer(ordonnance)
        return Response(serializer.data)