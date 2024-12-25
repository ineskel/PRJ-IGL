from rest_framework import permissions

class IsMedecin(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.role == 'medecin'

class IsAdministratif(permissions.BasePermission):
     
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False         
        role = getattr(request.user, 'role', None)   
        if role == 'administratif':
            return True   
        return False
    
class IsRadiologue(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.role == 'radiologue'
    
