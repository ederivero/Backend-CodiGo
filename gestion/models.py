from django.db import models

class Cabecera(models.Model):
    id = models.AutoField(primary_key=True, null=False)
    fecha = models.DateField(null=False)
    total = models.FloatField(null=False)
    dni = models.TextField()
    nombre = models.TextField()
    apellido = models.TextField()

    class Meta:
        db_table = 'cabeceras'

class Producto(models.Model):
    id = models.AutoField(primary_key=True, null=False)
    nombre = models.TextField(null=False)
    precio = models.FloatField(null=False)

    class Meta:
        db_table = 'productos'

class Detalle(models.Model):
    id = models.AutoField(primary_key=True, null=False)
    cantidad = models.IntegerField(null=False)
    subTotal = models.FloatField(null=False, db_column='sub_total')
    producto = models.ForeignKey(to=Producto, on_delete=models.RESTRICT, db_column='producto_id')
    cabecera = models.ForeignKey(to=Cabecera, on_delete=models.RESTRICT, db_column='cabecera_id')

    class Meta:
        db_table = 'detalles'