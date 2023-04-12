from rest_framework import serializers


class ItemsSerializer(serializers.Serializer):
    id = serializers.IntegerField(required=True)
    cantidad = serializers.IntegerField(required=True, min_value= 0)

class GenerarBoletaSerializer(serializers.Serializer):
    documento_usuario = serializers.CharField(max_length = 8, min_length=8, allow_null=False, required=True)
    nombre_usuario = serializers.CharField(required=True)
    items = ItemsSerializer(many=True)