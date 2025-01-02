from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from .models import User

class UserTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.administratif_user = User.objects.create_superuser(
            email='admin@example.com',
            password='adminpassword',
            nom='Admin',
            prenom='User',
            role='administratif',
            specialite=''
        )
        self.medecin_user = User.objects.create_user(
            email='medecin@example.com',
            password='medecinpassword',
            nom='Medecin',
            prenom='User',
            role='medecin',
            specialite='cardiologue'
        )
        self.patient_user = User.objects.create_user(
            email='patient@example.com',
            password='patientpassword',
            nom='Patient',
            prenom='User',
            role='patient',
            specialite=''
        )

    def test_register_valid_user(self):
        url = reverse('register')
        data = {
            'email': 'newmedecin@example.com',
            'password': 'newpassword',
            'nom': 'New',
            'prenom': 'Medecin',
            'role': 'medecin',
            'specialite': 'neurologue'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 4)
        self.assertEqual(User.objects.get(email=data['email']).role, 'medecin')

    def test_register_invalid_role(self):
        url = reverse('register')
        data = {
            'email': 'patient_try@example.com',
            'password': 'newpassword',
            'nom': 'New',
            'prenom': 'Patient',
            'role': 'patient',
            'specialite': ''
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('error', response.data)
        self.assertEqual(response.data['error'], 'Patient can not register')

    def test_login_valid_credentials(self):
        url = reverse('login')
        data = {
            'email': 'admin@example.com',
            'password': 'adminpassword'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)

    def test_login_invalid_credentials(self):
        url = reverse('login')
        data = {
            'email': 'admin@example.com',
            'password': 'wrongpassword'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('error', response.data)

    def test_change_password_valid(self):
        self.client.force_authenticate(user=self.administratif_user)
        url = reverse('change_password')
        data = {'password': 'newadminpassword'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('message', response.data)
        self.assertEqual(response.data['message'], 'Password changed successfully')

    def test_get_medecins_as_admin(self):
        self.client.force_authenticate(user=self.administratif_user)
        url = reverse('get_medecins')
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['role'], 'medecin')

    def test_get_patients(self):
        url = reverse('get_patients')
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['role'], 'patient')

    def test_get_users_as_admin(self):
        self.client.force_authenticate(user=self.administratif_user)
        url = reverse('get_users')
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 3)

    def test_get_users_as_non_admin(self):
        self.client.force_authenticate(user=self.medecin_user)
        url = reverse('get_users')
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
