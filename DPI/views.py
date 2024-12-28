from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from .models import DPI
from django.contrib.auth import get_user_model
from Compte.serializers import UserSerializer
from Compte.permissions import IsPatient, IsMedecin, IsAdministratif
from .serializers import DPISerializer, DPIDetailSerializer
from rest_framework.views import APIView
from django.utils.crypto import get_random_string
# Create your views here.

class DPIView(APIView):
    permission_classes = [IsAdministratif | IsMedecin ]
    def post(self, request):
        # get the data from the request to create the patient before creating the DPI
        data = request.data
        # generate a random password for the patient
        password = get_random_string(length=8)
        print(password)
        Patient={
            'nom': data['Nom'],
            'prenom': data['Prenom'],
            'email': data['email'],
            'role': 'patient',
            'password': password,
            'specialite': '',    
        }
        # create the patient
        serializer = UserSerializer(data=Patient)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        # create the DPI
        patient = serializer.save()  
        data["Patient"] = patient.id  
        serializer = DPISerializer(data=data)
        if not serializer.is_valid():
            # remove the patient from the database if the DPI creation fails
            patient.delete()
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
class DPIList(APIView):
    permission_classes = [IsAdministratif | IsMedecin ]
    def get(self, request):
        DPIs = DPI.objects.all()
        serializer = DPISerializer(DPIs, many=True)
        return Response(serializer.data)
    
class RechercheDPI(APIView):
    permission_classes = [IsPatient | IsMedecin]

    def get(self, request, NSS):
        try:
            # Check if the user is a patient
            if request.user.role == 'patient':
                # Ensure the patient can only access their own DPI
                dpi_instance = DPI.objects.select_related('Patient').get(NSS=NSS, Patient=request.user)
            else:
                # If not a patient, allow the user to access any DPI
                dpi_instance = DPI.objects.get(NSS=NSS)
        except DPI.DoesNotExist:
            # Return a 404 response if the DPI record does not exist
            return Response({"error": "DPI not found."}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            # Handle unexpected exceptions and return a 500 response
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        # Serialize the DPI instance and return the data
        serializer = DPISerializer(dpi_instance)
        return Response(serializer.data, status=status.HTTP_200_OK)


class ConsulterDPI(APIView):
    permission_classes = [IsPatient | IsMedecin]
    def get(self, request, NSS):
        try:
            # Check if the user is a patient
            if request.user.role == 'patient':
                # Ensure the patient can only access their own DPI
                dpi_instance = DPI.objects.prefetch_related(
                    'DPI_Soin', 'Consultation_DPI').select_related('Patient').get(NSS=NSS, Patient=request.user)
            else:
                # If not a patient, allow the user to access any DPI
                dpi_instance = DPI.objects.prefetch_related(
                    'DPI_Soin', 'Consultation_DPI').get(NSS=NSS)
        except DPI.DoesNotExist:
            # Return a 404 response if the DPI record does not exist
            return Response({"error": "DPI not found."}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            # Handle unexpected exceptions and return a 500 response
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        # Serialize the DPI instance and return the data
        serializer = DPIDetailSerializer(dpi_instance)
        # get the consultations of the patient
        return Response(serializer.data, status=status.HTTP_200_OK)