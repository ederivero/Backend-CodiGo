from rest_framework import generics, response, status, request, permissions
from .models import CategoriaModel, UsuarioModel
from .serializers import CategoriaSerializer, RegistroUsuarioSerializer, MostrarUsuarioSerializer
from .permissions import SoloAdministrador


class CategoriaApiView(generics.ListCreateAPIView):
    # SELECT * FROM categorias;
    permission_classes = [permissions.IsAuthenticated, SoloAdministrador]
    queryset = CategoriaModel.objects.all()
    serializer_class = CategoriaSerializer

class UnaCategoriaApiView(generics.RetrieveUpdateAPIView):
    def get(self, request, id):
        # SELECT * FROM categorias WHERE id = ...;
        resultado = CategoriaModel.objects.filter(id = id).first()
        if resultado is None:
            return response.Response(data={
                'message': 'La categoria no existe'
            }, status= status.HTTP_404_NOT_FOUND)
        
        serializador = CategoriaSerializer(instance=resultado)
        
        return response.Response(data={
            'message': serializador.data
        }, status=status.HTTP_200_OK)
    
    def put(self, request: request.Request, id):
        resultado = CategoriaModel.objects.filter(id = id).first()
        if resultado is None:
            return response.Response(data={
                'message': 'La categoria no existe'
            }, status= status.HTTP_404_NOT_FOUND)
        
        data_serializada = CategoriaSerializer(data= request.data)

        if data_serializada.is_valid():
            resultado.nombre = data_serializada.data.get('nombre')
            resultado.save()

            return response.Response(data={
                'message': 'Categoria actualizada exitosamente'
            })

        else:
            return response.Response(data={
                'message': 'Error al actualizar la categoria',
                'content': data_serializada.errors
            })

class RegistroUsuarioApiView(generics.CreateAPIView):
    def post(self, request: request.Request):
        serializador = RegistroUsuarioSerializer(data = request.data)

        if serializador.is_valid():
            nuevo_usuario = UsuarioModel(**serializador.validated_data)
            nuevo_usuario.set_password(serializador.validated_data.get('password'))

            nuevo_usuario.save()
            return response.Response(data={
                'message': 'Usuario creado exitosamente'
            }, status=status.HTTP_201_CREATED)
        else:
            return response.Response(data={
                'message': 'Error al registrar al usuario',
                'content': serializador.errors
            }, status=status.HTTP_400_BAD_REQUEST)

class PerfilUsuarioApiView(generics.RetrieveAPIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request: request.Request):
        print(request.user)
        print(request.auth)
        usuario_encontrado = MostrarUsuarioSerializer(instance= request.user)

        return response.Response(data={
            'content': usuario_encontrado.data
        })