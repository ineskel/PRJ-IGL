from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import UserSerializer
from .models import User
from rest_framework.permissions import AllowAny , IsAuthenticated
from .permissions import IsAdminUser 
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from Compte.permissions import IsAdministratif
from drf_yasg.utils import swagger_auto_schema
# Create your views here.

@api_view(['POST'])
@permission_classes([AllowAny])
@swagger_auto_schema(operation_description="Register a new user", request_body=UserSerializer)
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
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    return Response({'error': 'Invalid request'}, status=status.HTTP_400_BAD_REQUEST)
        

@api_view(['POST'])
@permission_classes([AllowAny])
@swagger_auto_schema(operation_description="Login a user", request_body=UserSerializer , responses={200: UserSerializer})
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
    
    
    
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def change_password(request):
    user = request.user
    password = request.data.get('password')

    if not password:
        return Response({'error': 'Password is required'}, status=status.HTTP_400_BAD_REQUEST)

    # Validate the password
    try:
        validate_password(password, user=user)
    except ValidationError as e:
        return Response({'errors': e.messages}, status=status.HTTP_400_BAD_REQUEST)

    # Set and save the new password
    user.set_password(password)
    user.save()

    return Response({'message': 'Password changed successfully'}, status=status.HTTP_200_OK)

@api_view(['GET'])
@permission_classes([IsAdminUser])
def get_medecins(request):
    medecins = User.objects.filter(role='medecin')
    serializer = UserSerializer(medecins, many=True)
    return Response(serializer.data)



@api_view(['GET'])
@permission_classes([AllowAny])
def get_patients(request):
    try:
        patients = User.objects.filter(role='patient')
        serializer = UserSerializer(patients, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
@permission_classes([IsAdministratif])
def get_users(request):
    users = User.objects.all()
    serializer = UserSerializer(users, many=True)
    return Response(serializer.data)