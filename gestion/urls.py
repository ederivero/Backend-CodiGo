from django.urls import path
from .views import GenerarBoleta, GenerarPago, webhooks_mp

urlpatterns = [
    path('generar-boleta', GenerarBoleta.as_view()),
    path('consultar-boleta/<str:serie>/<int:numero>', GenerarBoleta.as_view()),
    path('generar-pago', GenerarPago.as_view()),
    path('webhooks-mp', webhooks_mp)
]