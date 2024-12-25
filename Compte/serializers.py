from rest_framework import serializers
from .models import User
from django.core.mail import send_mail

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'nom','prenom', 'email', 'role', 'specialite', 'password']
        extra_kwargs = {
            'password': {'write_only': True},  
        }

    def create(self, validated_data):
        """
        Custom create method to handle user creation with the specified fields.
        """
        user = User.objects.create_user(
            email=validated_data['email'],
            password=validated_data['password'],
            nom=validated_data.get('nom', ''),
            prenom=validated_data.get('prenom', ''),
            role=validated_data.get('role'),
            specialite=validated_data.get('specialite'),
        )
        user.save()
        
               # Send a welcome email
        subject = 'Welcome to Our Platform!'
        message = f"Hello {user.nom} {user.prenom},\n\n" \
                  f"Your account has been created. Here are your login details:\n" \
                  f"Email: {user.email}\n" \
                  f"Password: {validated_data['password']}\n\n" \
                  f"Please change your password after logging in."

        from_email = 'noreply@example.com'  # Sender email
        recipient_list = [user.email]  # List of recipient emails

        send_mail(subject, message, from_email, recipient_list)
        return user
    
    
            