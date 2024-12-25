from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models


class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        """
        Required fields: nom, prenom, role, specialite, and email
        """
        if not email:
            raise ValueError('Email is required.')
        if not extra_fields.get('nom'):
            raise ValueError('The "nom" field is required.')
        if not extra_fields.get('prenom'):
            raise ValueError('The "prenom" field is required.')
        if not extra_fields.get('role'):
            raise ValueError('The "role" field is required.')

        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        """
        Create and return a superuser.
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    """
    Custom user model with roles and specialties.
    """
    # Basic fields
    id = models.AutoField(primary_key=True)
    nom = models.CharField(max_length=150)
    prenom = models.CharField(max_length=150)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=128)

    # Additional fields
    ROLE_CHOICES = [
        ('patient', 'Patient'),
        ('medecin', 'Medecin'),
        ('radiologue', 'Radiologue'),
        ('laborantin', 'Laborantin'),
        ('infirmier', 'Infirmier'),
        ('administratif', 'Administratif'),
    ]
    role = models.CharField(max_length=15, choices=ROLE_CHOICES)

    SPECIALITY_CHOICES = [
        ('pediatre', 'Pédiatre'),
        ('cardiologue', 'Cardiologue'),
        ('ophtalmologue', 'Ophtalmologue'),
        ('neurologue', 'Neurologue'),
        ('urologue', 'Urologue'),
        ('gynecologue', 'Gynécologue'),
        ('', 'None'),
    ]
    specialite = models.CharField(max_length=20, choices=SPECIALITY_CHOICES)

    # Fields for user management
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['nom', 'prenom', 'role', 'specialite']

    def __str__(self):
        return self.nom
