from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import DPISerializer
from .models import DPI , Patient


class DPIView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = DPISerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def get(self, request, *args, **kwargs):
        dpi_objects = DPI.objects.all()
        serializer = DPISerializer(dpi_objects, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)



# View to get a single DPI by NSS
class DPIByNSSView(APIView):
    def get(self, request, NSS, *args, **kwargs):
        try:
            dpi = DPI.objects.get(NSS=NSS)
            serializer = DPISerializer(dpi)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except DPI.DoesNotExist:
            return Response(
                {"error": "DPI with the specified NSS does not exist."},
                status=status.HTTP_404_NOT_FOUND
            )
        
class PatientAuthView(APIView):
    def post(self, request, *args, **kwargs):
        identifier = request.data.get("identifier")  # Can be NSS or email
        password = request.data.get("Password")

        if not identifier or not password:
            return Response(
                {"error": "Identifier (NSS or email) and Password are required fields."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            # Check if identifier is NSS (numeric) or email (contains '@')
            if identifier.isdigit():
                # Authenticate by NSS
                patient = Patient.objects.get(DPI_NSS__NSS=identifier)
            else:
                # Authenticate by email
                patient = Patient.objects.get(email=identifier)

            # Verify password
            if patient.Password == password:  # Replace with hashed password check if needed
                # Retrieve associated DPI
                dpi = patient.DPI_NSS
                serializer = DPISerializer(dpi)
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response(
                    {"error": "Invalid password."},
                    status=status.HTTP_401_UNAUTHORIZED,
                )
        except Patient.DoesNotExist:
            return Response(
                {"error": "Patient with the specified identifier does not exist."},
                status=status.HTTP_404_NOT_FOUND,
            )


