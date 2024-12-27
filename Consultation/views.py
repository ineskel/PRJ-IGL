from rest_framework import status
from rest_framework.response import Response
from .models import Consultation
from Compte.permissions import IsMedecin ,IsLaborantin ,IsRadiologue
from .serializers import ConsultationCreateSerializer
from rest_framework.decorators import api_view, permission_classes
from Ordonnance.models import Ordonnance
from Bilan.models import BilanBiologique, BilanRadiologique

# Create your views here.

# create consultation 
@api_view(['POST'])
@permission_classes([IsMedecin])
def create_consultation(request):
    medecin = request.user
    data = request.data
    data['medecin'] = medecin.id
    serializer = ConsultationCreateSerializer(data=data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# get all consultations
@api_view(['GET'])
@permission_classes([IsMedecin])
def get_consultations(request):
    medecin = request.user
    consultations = Consultation.objects.filter(medecin=medecin)
    serializer = ConsultationCreateSerializer(consultations, many=True)
    return Response(serializer.data)

# get consultation by id for medecin
@api_view(['GET'])
@permission_classes([IsMedecin])
def get_consultation_medecin(request, pk):
    medecin = request.user
    consultation = Consultation.objects.get(medecin=medecin, id=pk)
    if consultation:
        serializer = ConsultationCreateSerializer(consultation)
        return Response(serializer.data)
    return Response({'error': 'Consultation not found'}, status=status.HTTP_404_NOT_FOUND)
# update consultation
@api_view(['PUT'])
@permission_classes([IsMedecin])
def UpdateConsultation(request, pk):
    medecin = request.user
    consultation = Consultation.objects.filter(medecin=medecin, id=pk)
    if consultation:
        data = request.data
        data['medecin'] = medecin.id
        serializer = ConsultationCreateSerializer(consultation, data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    return Response({'error': 'Consultation not found'}, status=status.HTTP_404_NOT_FOUND)

# add ordonnance to consultation
@api_view(['POST'])
@permission_classes([IsMedecin])
def add_ordonnance(request, pk):
    medecin = request.user
    consultation = Consultation.objects.filter(medecin=medecin, id=pk)
    if consultation:
        data = request.data
        data['medecin'] = medecin.id
        data['consultation'] = pk
        serializer = ConsultationCreateSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    return Response({'error': 'Consultation not found'}, status=status.HTTP_404_NOT_FOUND)

# add bilan biologique to consultation
@api_view(['POST'])
@permission_classes([IsLaborantin])
def add_bilan_biologique(request, pk):
    laborantin = request.user
    consultation = Consultation.objects.filter(id=pk)
    if consultation:
        data = request.data
        data['laborantin'] = laborantin.id
        data['consultation'] = pk
        serializer = ConsultationCreateSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    return Response({'error': 'Consultation not found'}, status=status.HTTP_404_NOT_FOUND)

# add bilan radiologique to consultation
@api_view(['POST'])
@permission_classes([IsRadiologue])
def add_bilan_radiologique(request, pk):
    radiologue = request.user
    consultation = Consultation.objects.filter(id=pk)
    if consultation:
        data = request.data
        data['radiologue'] = radiologue.id
        data['consultation'] = pk
        serializer = ConsultationCreateSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    return Response({'error': 'Consultation not found'}, status=status.HTTP_404_NOT_FOUND)