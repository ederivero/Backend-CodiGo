from psycopg2 import connect

conexion = connect("dbname=pruebas user=postgres password=root")

cursor = conexion.cursor()

cursor.execute("SELECT * FROM productos;")

respuesta = cursor.fetchall()
print(respuesta)