from django.urls import path
from .views import CategoriaApiView, UnaCategoriaApiView, RegistroUsuarioApiView, PerfilUsuarioApiView
from rest_framework_simplejwt.views import TokenObtainPairView

urlpatterns = [
    path('categoria', CategoriaApiView.as_view()),
    path('categoria/<int:id>', UnaCategoriaApiView.as_view()),
    path('registro', RegistroUsuarioApiView.as_view()),
    path('login', TokenObtainPairView.as_view()),
    path('perfil', PerfilUsuarioApiView.as_view())
]