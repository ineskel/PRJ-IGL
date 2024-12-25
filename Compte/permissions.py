from rest_framework import permissions

"""  ROLE_CHOICES = [
        ('patient', 'Patient'),
        ('medecin', 'Medecin'),
        ('radiologue', 'Radiologue'),
        ('laborantin', 'Laborantin'),
        ('infirmier', 'Infirmier'),
        ('administratif', 'Administratif'),
    ]
"""
class IsSuperUser(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated and request.user.is_superuser
class IsPatient(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.role == 'patient'   
class IsMedecin(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated and request.user.role == 'medecin'   
class IsAdministratif(permissions.BasePermission):  
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated and request.user.role == 'administratif'
class IsInfermier(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated and request.user.role == 'infermier' 
class IsRadiologue(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated and request.user.role == 'radiologue'
class IsLaborantin(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated and request.user.role == 'laborantin'

       


     

