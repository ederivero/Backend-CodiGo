from flask import Flask, request
from flask_cors import CORS

# indicar si nuestro archivo es el archivo principal , si el archivo es el principal su valor sera '__main__'
app = Flask(__name__)

CORS(app, resources=['*'], allow_headers=['*'], methods=['GET', 'POST', 'PUT', 'DELETE'])

productos = [
    {
        'nombre':'Platano',
        'precio': 3.50
    },
    {
        'nombre':'Sandia',
        'precio': 2.80
    },
    {
        'nombre':'Tomate',
        'precio': 2.30
    },
]

@app.route('/')
def inicio():
    # modificar el comportamiento del metodo route de la clase Flask para evitar modificar el metodo en la misma clase
    print('hola')
    return 'Bienvenido a mi aplicacion de flask'

@app.route('/productos', methods= ['GET', 'POST'])
def gestion_productos():
    print(request.method)
    if request.method == 'GET':
        return {
            'content': productos
        }

    elif request.method == 'POST':
        # get_json() > convierte la data entrante a un formato diccionario
        print(request.get_json())
        data = request.get_json()
        
        productos.append(data)
        return {
            'message': 'Producto creado exitosamente'
        }

@app.route('/producto/<int:id>', methods=['GET', 'PUT', 'DELETE'])
def gestion_producto(id):
    if request.method=='GET':
        limite = len(productos)
        if limite < id:
            return {
                'message': 'El producto no existe'
            }
        else:
            return {
                'content': productos[id]
            }
    elif request.method == 'PUT':
        limite = len(productos)
        if limite < id:
            return {
                'message': 'El producto no existe'
            }
        else:
            data = request.get_json()
            productos[id] = data
            return {
                'message': 'Producto actualizado exitosamente'
            }
    elif request.method == 'DELETE':
        limite = len(productos)
        if limite < id:
            return {
                'message': 'El producto no existe'
            }
        else:
            del productos[id]
            return {
                'message': 'Producto eliminado exitosamente'
            }

if __name__ == '__main__':
    app.run(debug=True)
