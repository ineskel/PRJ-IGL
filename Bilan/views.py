from rest_framework import status
from rest_framework.response import Response
from Compte.permissions import IsLaborantin , IsRadiologue , IsMedecin
from .serializers import BilanBiologiqueSerializer, BilanRadiologiqueSerializer , DemandeBilanSerializer
from rest_framework.decorators import api_view, permission_classes
from .models import  DemandeBilan
# add documentation 
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi


# create BilanBiolgique 
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

@api_view(['POST'])
@permission_classes([IsRadiologue])
def create_bilanradiologique(request, pk):
    """
    Create a new Bilan Radiologique record for the specified consultation.
    
    - `radiologue`: The user making the request (assigned automatically).
    - `Consultation`: The ID of the consultation this record is associated with.
    """
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

# create DemandeBilan
@api_view(['POST'])
@permission_classes([IsMedecin])
def create_demandebilan(request):
    """
    Create a new Demande Bilan record for a specific patient.
    
    - `medecin`: The user making the request (assigned automatically).
    - `patient`: The ID of the patient this record is associated with.
    - `typebilan`: The type of bilan requested (B: Biologique, R: Radiologique).
    """
    medecin = request.user
    data = request.data
    data['medecin'] = medecin.id
    # Create the DemandeBilan instance
    serializer = DemandeBilanSerializer(data=data)
    if serializer.is_valid():
        # Save the DemandeBilan
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# get all demandes de bilan
@api_view(['GET'])
@permission_classes([IsMedecin | IsLaborantin | IsRadiologue])
def getdemandesbilan(request):
    """
    Get all Demande Bilan records.
    
    - `medecin`: Get all demandes bilan.
    - `laborantin`: Get all demandes bilan biologique.
    - `radiologue`: Get all demandes bilan radiologique.
    """
    user = request.user
    if user.role == 'medecin':
        demandes = DemandeBilan.objects.all()
    elif user.role == 'laborantin':
        demandes = DemandeBilan.objects.filter(etat='enattente',typebilan='B')
    elif user.role == 'radiologue':
        demandes = DemandeBilan.objects.filter(etat='enattente',typebilan='R')
    else:
        return Response({'error': 'User not allowed to access this resource'}, status=status.HTTP_403_FORBIDDEN)
    serializer = DemandeBilanSerializer(demandes, many=True)
    return Response(serializer.data)

# take a demandes de bilan
@api_view(['PUT'])
@permission_classes([IsLaborantin | IsRadiologue])
def treatdemandesbilan(request, pk):
    """ 
    Treat a specific Demande Bilan record.
    
    - `laborantin`: Treat demandes bilan biologique.
    - `radiologue`: Treat demandes bilan radiologique.
    Args:
    request: Request.user and Demande Bilan record ID.
    pk: Demande Bilan record ID.

    Returns:
       Demande: Demande Bilan record.
    """
    user = request.user
    demande = DemandeBilan.objects.get(pk=pk)
    if user.role == 'laborantin' and demande.typebilan == 'B':
        demande.etat = 'traitee'
    elif user.role == 'radiologue' and demande.typebilan == 'R':
        demande.etat = 'traitee'
    else:
        return Response({'error': 'User not allowed to access this resource'}, status=status.HTTP_403_FORBIDDEN)
    demande.save()
    serializer = DemandeBilanSerializer(demande)
    return Response(serializer.data)