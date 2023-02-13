import pytest 
from flask import Flask
from app import app

@pytest.fixture()
def cliente():
    client = app.test_client()
    yield client

def test_actividades_get(cliente: Flask):
    respuesta = cliente.get('/actividades')
    assert respuesta.json == {
        'message': 'Internal Server Error'
    }

def test_registro(cliente: Flask):
    respuesta = cliente.post('/registro', json = {
        'nombre':'Juan',
        'apellido': 'Vargas',
        'correo': 'jvargas@correo.com',
        'password': 'Welcome123!'
    })

    assert respuesta.status_code == 201
    assert 'message' in respuesta.json
    assert respuesta.json.get('message') == 'Usuario registrado exitosamente'

def test_login(cliente: Flask):
    respuesta = cliente.post('/login', json = {
        'correo': 'jvargas@correo.com',
        'password': 'Welcome123!'
    })
    assert 'content' in respuesta.json
    assert respuesta.status_code == 200


def test_actividades_get_autorizado(cliente: Flask):
    respuesta_login = cliente.post('/login', json = {
        'correo': 'jvargas@correo.com',
        'password': 'Welcome123!'
    })
    token = respuesta_login.json.get('content')

    respuesta = cliente.get('/actividades', headers = {'Authorization': 'Bearer {}'.format(token)})
    assert respuesta.json == {
        'content': []
    }