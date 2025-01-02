from rest_framework import status
from rest_framework.response import Response
from Compte.permissions import IsInfermier , IsPatient
from .models import Soin
from .serializers import SoinsCreateSerializer, SoinsSerializer
from rest_framework.decorators import api_view, permission_classes
from DPI.models import DPI
# Create your views here.

# create soin
@api_view(['POST'])
@permission_classes([IsInfermier])
def create_soin(request):
    infermier = request.user
    data = request.data
    data['infermier'] = infermier.id
    # Create the soin instance
    serializer = SoinsSerializer(data=data)
    if serializer.is_valid():
        # Save the soin
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# update soin
@api_view(['PUT', 'DELETE'])
@permission_classes([IsInfermier])
def update_soin(request, IdSoin):
    try:
        soin = Soin.objects.get(IdSoin=IdSoin)
    except Soin.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    if request.method == 'PUT':
        serializer = SoinsSerializer(soin, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        soin.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)