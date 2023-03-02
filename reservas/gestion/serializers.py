from rest_framework import serializers
from .models import CategoriaModel, UsuarioModel


class CategoriaSerializer(serializers.ModelSerializer):
    class Meta:
        model = CategoriaModel
        fields = '__all__'


class RegistroUsuarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = UsuarioModel
        fields = '__all__'

class MostrarUsuarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = UsuarioModel
        exclude = ['password','is_staff', 'user_permissions', 'groups', 'last_login', 'is_superuser']

