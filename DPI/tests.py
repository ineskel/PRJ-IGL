import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from django.contrib.auth import get_user_model
from DPI.models import DPI
from datetime import date
import json

User = get_user_model()

@pytest.fixture
def api_client():
    return APIClient()

@pytest.fixture
def administratif_user():
    return User.objects.create_user(
        email='admin@test.com',
        password='testpass123',
        role='administratif',
        nom='Admin',
        prenom='User',
        specialite=''
    )

@pytest.fixture
def medecin_user():
    return User.objects.create_user(
        email='doctor@test.com',
        password='testpass123',
        role='medecin',
        nom='Doctor',
        prenom='User',
        specialite='Cardiology'
    )

@pytest.fixture
def patient_user():
    return User.objects.create_user(
        email='patient@test.com',
        password='testpass123',
        role='patient',
        nom='Patient',
        prenom='User',
        specialite=''
    )

@pytest.fixture
def sample_dpi(patient_user):
    return DPI.objects.create(
        NSS=1234567890,
        Nom='Test',
        Prenom='Patient',
        DateDeNaissonce=date(1990, 1, 1),
        Adress='123 Test St',
        Numero='0123456789',
        Mutuelle='Test Mutuelle',
        sexe='M',
        ContactNom='Emergency Contact',
        ContactNumero='9876543210',
        Patient=patient_user
    )

@pytest.mark.django_db
class TestDPIModel:
    def test_dpi_creation(self, sample_dpi):
        assert sample_dpi.NSS == 1234567890
        assert str(sample_dpi) == "Test Patient"

    def test_dpi_patient_relationship(self, sample_dpi, patient_user):
        assert sample_dpi.Patient == patient_user
        assert patient_user.DPI_Patient == sample_dpi

@pytest.mark.django_db
class TestDPIViews:
    def test_create_dpi_admin(self, api_client, administratif_user):
        api_client.force_authenticate(user=administratif_user)
        url = reverse('CreateDPI')
        data = {
            'NSS': 9876543210,
            'Nom': 'New',
            'Prenom': 'Patient',
            'DateDeNaissonce': '1995-01-01',
            'Adress': '456 New St',
            'Numero': '0123456789',
            'Mutuelle': 'New Mutuelle',
            'sexe': 'F',
            'ContactNom': 'New Emergency',
            'ContactNumero': '1234567890',
            'email': 'new.patient@test.com'
        }
        
        response = api_client.post(url, data, format='json')
        assert response.status_code == status.HTTP_201_CREATED
        assert DPI.objects.filter(NSS=9876543210).exists()

    def test_list_dpi_doctor(self, api_client, medecin_user, sample_dpi):
        api_client.force_authenticate(user=medecin_user)
        url = reverse('DPIs')
        response = api_client.get(url)
        
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 1

    def test_search_dpi_patient_own_record(self, api_client, patient_user, sample_dpi):
        api_client.force_authenticate(user=patient_user)
        url = reverse('RechercheDPI', kwargs={'NSS': sample_dpi.NSS})
        response = api_client.get(url)
        
        assert response.status_code == status.HTTP_200_OK
        assert response.data['NSS'] == sample_dpi.NSS

    def test_search_dpi_patient_other_record(self, api_client, patient_user):
        other_patient = User.objects.create_user(
            email='other.patient@test.com',
            password='testpass123',
            role='patient',
            nom='Other',
            prenom='Patient',
            specialite=''
        )
        other_dpi = DPI.objects.create(
            NSS=9999999999,
            Nom='Other',
            Prenom='Patient',
            DateDeNaissonce=date(1990, 1, 1),
            Adress='789 Other St',
            Numero='9999999999',
            Mutuelle='Other Mutuelle',
            sexe='F',
            ContactNom='Other Emergency',
            ContactNumero='8888888888',
            Patient=other_patient
        )
        
        api_client.force_authenticate(user=patient_user)
        url = reverse('RechercheDPI', kwargs={'NSS': other_dpi.NSS})
        response = api_client.get(url)
        
        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_consulter_dpi_doctor(self, api_client, medecin_user, sample_dpi):
        api_client.force_authenticate(user=medecin_user)
        url = reverse('ConsulterDPI', kwargs={'NSS': sample_dpi.NSS})
        response = api_client.get(url)
        
        assert response.status_code == status.HTTP_200_OK
        assert 'dpi' in response.data
        assert 'consultations' in response.data
        assert 'soins' in response.data

@pytest.mark.django_db
class TestDPISerializer:
    def test_dpi_serializer_valid_data(self, patient_user):
        from DPI.serializers import DPISerializer
        
        valid_data = {
            'NSS': 1111111111,
            'Nom': 'Test',
            'Prenom': 'Serializer',
            'DateDeNaissonce': '1990-01-01',
            'Adress': 'Test Address',
            'Numero': '1234567890',
            'Mutuelle': 'Test Mutuelle',
            'sexe': 'M',
            'ContactNom': 'Test Contact',
            'ContactNumero': '0987654321',
            'Patient': patient_user.id  # Use the id of the created patient
        }
        
        serializer = DPISerializer(data=valid_data)
        assert serializer.is_valid() == True

    def test_dpi_serializer_invalid_data(self):
        from DPI.serializers import DPISerializer
        
        invalid_data = {
            'NSS': 'not-a-number',  # Should be an integer
            'Nom': '',  # Required field
            'sexe': 'X'  # Invalid choice
        }
        
        serializer = DPISerializer(data=invalid_data)
        assert serializer.is_valid() == False
        assert 'NSS' in serializer.errors
        assert 'Nom' in serializer.errors
        assert 'sexe' in serializer.errors