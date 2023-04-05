from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from .auth_manager import UsuarioManager
# Create your models here.
class CategoriaModel(models.Model):
    id = models.AutoField(primary_key=True, unique=True, null=False)
    nombre = models.CharField(max_length=100, unique=True, null=False)
    # campos de auditoria
    # creados automaticamente por la base de datos en el cual el backend no interfiere en nada solo para visualizacion
    createdAt = models.DateTimeField(auto_now_add=True, db_column='created_at')
    # se modificara el valor cada vez que hagamos una modificacion a las otras columnas con la fecha y hora actual
    updatedAt = models.DateTimeField(auto_now=True, db_column='updated_at')

    class Meta:
        db_table = 'categorias'


class ProductoModel(models.Model):
    id = models.AutoField(primary_key=True, unique=True, null=False)
    nombre = models.CharField(max_length=100, null=False)
    precio = models.FloatField()
    disponible = models.BooleanField(default=True)

    createdAt = models.DateTimeField(auto_now_add=True, db_column='created_at')

    # relaciones
    categoria = models.ForeignKey(to=CategoriaModel, on_delete=models.CASCADE, db_column='categoria_id')

    class Meta:
        db_table = 'productos'


class UsuarioModel(AbstractBaseUser, PermissionsMixin):
    id = models.AutoField(primary_key=True, unique=True)
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    correo = models.EmailField(max_length=100, unique=True, null=False)
    password = models.TextField(null=False)

    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    tipoUsuario = models.CharField(max_length=100, choices= [('ADMIN', 'ADMIN'), ('TRABAJADOR', 'TRABAJADOR')], default='ADMIN', db_column='tipo_usuario')
    
    createdAt = models.DateTimeField(auto_now_add=True, db_column='created_at')

    # si queremos ingresar al panel administrativo que atributo utilizara para pedirle al usuario
    USERNAME_FIELD = 'correo'

    # cuando queremos crear un superusuario por la terminal que atributos nos debe de solicitar
    REQUIRED_FIELDS = ['nombre', 'apellido']

    objects = UsuarioManager()

    class Meta:
        db_table='usuarios'