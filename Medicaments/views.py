from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Medicament
from .serializers import MedicamentSerializer

class MedicamentList(APIView): 
    def get(self, request):
        medicaments = Medicament.objects.all()
        serializer = MedicamentSerializer(medicaments, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = MedicamentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    def delete(self, request, pk):
        medicament = Medicament.objects.get(pk=pk)
        medicament.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    