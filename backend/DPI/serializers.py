from rest_framework import serializers
from django.core.mail import send_mail
from django.utils.crypto import get_random_string
from .models import DPI, Patient

class DPISerializer(serializers.ModelSerializer):
    email = serializers.EmailField(write_only=True)  # Accept email in the form

    class Meta:
        model = DPI
        fields = [
            'NSS', 'Nom', 'Prenom', 'DateDeNaissonce', 'Adress', 'Numero',
            'Mutuelle', 'sexe', 'ContactNom', 'ContactNumero', 'created_at',
            'updated_at', 'email'  # Include email for Patient creation
        ]
        read_only_fields = ['created_at', 'updated_at']

    def create(self, validated_data):
        # Extract email from validated_data
        email = validated_data.pop('email')
        
        # Create DPI instance
        dpi_instance = DPI.objects.create(**validated_data)

        # Generate a random password for the patient
        password = get_random_string(length=8)

        # Create the Patient instance linked to this DPI
        Patient.objects.create(
            DPI_NSS=dpi_instance,
            email=email,
            Password=password
        )

        # Send the password to the user via email
        send_mail(
            subject='Welcome to Our System',
            message=f"Hello {dpi_instance.Nom} {dpi_instance.Prenom},\n\n"
                    f"Your account has been created. Here are your login details:\n"
                    f"Email: {email}\n"
                    f"Password: {password}\n\n"
                    f"Please change your password after logging in.",
            from_email='noreply@example.com',
            recipient_list=[email],
        )

        return dpi_instance
