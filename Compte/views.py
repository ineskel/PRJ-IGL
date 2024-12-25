from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import UserSerializer
from .models import User
from rest_framework.permissions import AllowAny
from .permissions import IsMedecin, IsAdministratif
# Create your views here.

@api_view(['POST'])
@permission_classes([AllowAny])
def register(request):
    if request.method == 'POST':
        serializer = UserSerializer(data=request.data)
        """
          check the role in the  request data 
          if the role is Patient then he can't register
          """
        if serializer.is_valid():
            if serializer.validated_data.get('role') == 'patient':
                return Response({'error': 'Patient can not register'}, status=status.HTTP_400_BAD_REQUEST)
            if 'specialite' not in request.data:
                request.data['specialite'] = ''
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        

@api_view(['POST'])
@permission_classes([AllowAny])
def login(request):

    if request.method == 'POST':
        email = request.data.get('email')
        password = request.data.get('password')
        user = authenticate(email=email, password=password)
        if user:
            refresh = RefreshToken.for_user(user)
            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
                'user':  UserSerializer(user).data
            })
        return Response({'error': 'Invalid credentials'}, status=status.HTTP_400_BAD_REQUEST)