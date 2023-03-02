from rest_framework.permissions import BasePermission

class SoloAdministrador(BasePermission):
    message = 'Solo los administradores puede acceder a estas rutas'
    
    def has_permission(self, request, view):
        # request.user > devolvia el usuario identificado
        tipoUsuario = request.user.tipoUsuario
        if tipoUsuario == 'ADMIN':
            return True
        
        else: 
            return False