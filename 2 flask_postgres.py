from flask import Flask
from psycopg2 import connect

app = Flask(__name__)

def conexion_bd():
    conexion = connect(host='localhost', database='pruebas', user='postgres', password='root')
    return conexion


@app.route('/', methods=['GET'])
def productos():
    conexion = conexion_bd()
    cursor = conexion.cursor()
    cursor.execute("SELECT * FROM productos;")
    resultado = cursor.fetchall()
    resultado_legible = []
    for registro in resultado:
        print(registro)
        producto = {
            'id': registro[0],
            'nombre': registro[1]
        }
        resultado_legible.append(producto)

    return {
        'content': resultado_legible
    }


app.run(debug=True)