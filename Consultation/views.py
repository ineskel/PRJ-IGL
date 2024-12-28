from rest_framework import status
from rest_framework.response import Response
from .models import Consultation
from Compte.permissions import IsMedecin , IsPatient
from .serializers import ConsultationCreateSerializer, ConsultationSerializer
from rest_framework.decorators import api_view, permission_classes
from Bilan.serializers import BilanBiologiqueSerializer, BilanRadiologiqueSerializer
# Create your views here.

# create consultation 
@api_view(['POST'])
@permission_classes([IsMedecin])
def create_consultation(request):
    medecin = request.user
    data = request.data
    data['medecin'] = medecin.id

    # Create the consultation instance
    serializer = ConsultationSerializer(data=data)
    if serializer.is_valid():
        # Save the consultation
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# get all consultations
@api_view(['GET'])
@permission_classes([IsMedecin])
def get_consultations(request):
    medecin = request.user
    consultations = Consultation.objects.filter(medecin=medecin)
    serializer = ConsultationSerializer(consultations, many=True)
    return Response(serializer.data)

# get consultation by id 
@api_view(['GET'])
# permision to medecin or patient
@permission_classes([IsMedecin | IsPatient])
def get_consultation_byid(request, pk):
    user = request.user
    if user.role == 'medecin':
        consultation = Consultation.objects.get(medecin=user, IdConsultation=pk)
    else:
        consultation = Consultation.objects.get(patient=user, IdConsultation=pk)
    if consultation:
        BilanBiologique = consultation.BilanBiologique_Consultation.all()
        BilanRadiologique = consultation.BilanRadiologique_Consultation.all()
        return Response({
        'consultation': ConsultationSerializer(consultation).data, 
        'BilanBiologique': BilanBiologiqueSerializer(BilanBiologique, many=True).data,
        'BilanRadiologique': BilanRadiologiqueSerializer(BilanRadiologique, many=True).data
        })
    return Response({'error': 'Consultation not found'}, status=status.HTTP_404_NOT_FOUND)
# update consultation
@api_view(['PUT'])
@permission_classes([IsMedecin])
def UpdateConsultation(request, pk):
    medecin = request.user
    consultation = Consultation.objects.filter(medecin=medecin, IdConsultation=pk)
    if consultation:
        data = request.data
        data['medecin'] = medecin.id
        serializer = ConsultationCreateSerializer(consultation, data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    return Response({'error': 'Consultation not found'}, status=status.HTTP_404_NOT_FOUND)




