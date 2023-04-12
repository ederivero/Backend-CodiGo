from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework.request import Request
from rest_framework.response import Response
from datetime import datetime
import requests
import mercadopago
from os import environ
from .serializers import GenerarBoletaSerializer
from .models import *


class GenerarBoleta(APIView):
    def post(self, request : Request):
        serializador = GenerarBoletaSerializer(data= request.data)

        serializador.is_valid(raise_exception=True)
        body = serializador.validated_data
        items = []
        total_general = 0
        total_igv = 0
        for item in body.get('items'):
            
            producto_encontrado = Producto.objects.filter(id = item.get('id')).first()
            if not producto_encontrado:
                return Response(data={
                    'message': 'El producto no existe'
                })
            base = producto_encontrado.precio / 1.18

            producto = {
                'unidad_de_medida': 'NIU',
                'codigo': producto_encontrado.id,
                'descripcion': producto_encontrado.nombre,
                'cantidad': item.get('cantidad'),
                'valor_unitario': base, # No tiene IGV
                'precio_unitario': producto_encontrado.precio, # Si tiene IGV
                'subtotal': base * item.get('cantidad'),
                'tipo_de_igv': 1,
                'igv': (producto_encontrado.precio - base)* item.get('cantidad'),
                'total': producto_encontrado.precio * item.get('cantidad'),
                'anticipo_regularizacion': False,
            }

            total_general += producto_encontrado.precio * item.get('cantidad')
            total_igv += (producto_encontrado.precio - base) * item.get('cantidad')
            items.append(producto)

        data = {
            'operacion': 'generar_comprobante',
            'tipo_de_comprobante': 2,
            'serie': 'BBB1',
            'numero': 1,
            'sunat_transaction': 1,
            'cliente_tipo_de_documento': 1,
            'cliente_numero_de_documento': body.get('documento_usuario'),
            'cliente_denominacion': body.get('nombre_usuario'),
            'fecha_de_emision': datetime.now().strftime('%d-%m-%Y'),
            'moneda': 1,
            'total_igv': total_igv,
            'total_gravada': total_general - total_igv,
            'porcentaje_de_igv': 18.00,
            'total': total_general,
            'items': items
        }

        peticion = requests.post(url=environ.get('NUBEFACT_URL'), headers={
            'Authorization': 'Bearer '+environ.get('NUBEFACT_TOKEN')
        },json=data)

        print(peticion.status_code)
        print(peticion.json())

        return Response(data={
            'message': 'Boleta creada exitosamente'
        })

    def get(self, request:Request, serie, numero):
        data = {
            'operacion': 'consultar_comprobante',
            'tipo_de_comprobante': 2,
            'serie': serie,
            'numero': numero
        }

        peticion = requests.post(url = environ.get('NUBEFACT_URL'), headers={ 
            'Authorization': 'Bearer ' + environ.get('NUBEFACT_TOKEN')}, json=data)
        
        print(peticion.json())
        resultado = peticion.json()

        return Response(data={
            'content': resultado
        })


class GenerarPago(APIView):
    def post(self, request :Request):
        sdk = mercadopago.SDK(environ.get('MERCADOPAGO_TOKEN'))

        respuesta = sdk.preference().create({
            "items": [{
                "title": "Audifonos",
                "description": "Hermosos audifonos bluethooth",
                "quantity": 1,
                # "currency_id": "PEN",
                "unit_price": 89.5,
                "id": 1
            }],
            "notification_url": "https://3825-179-6-165-235.ngrok-free.app/webhooks-mp"
        })
        print(respuesta)
        return Response(data={
            'content': respuesta 
        })

@api_view(http_method_names=['GET', 'POST'])
def webhooks_mp(request:Request):
    print(request.data)
    print(request.query_params)

    return Response(data={
        'message': 'Webhooks recibidos exitosamente'
    }, status= 200)