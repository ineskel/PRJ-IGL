from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import DPISerializer
from .models import DPI


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