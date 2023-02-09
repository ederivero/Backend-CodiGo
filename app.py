from flask import Flask
from sqlalchemy import Column, types
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql.schema import ForeignKey
from datetime import datetime, timedelta
from flask_restful import Resource, request, Api
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from marshmallow import Schema, fields
from bcrypt import hashpw, gensalt, checkpw
from flask_jwt_extended import create_access_token, JWTManager, jwt_required, get_jwt_identity
from correos import olvide_password
from cryptography.fernet import Fernet
from os import environ
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = environ.get('DATABASE_URL')
app.config['JWT_SECRET_KEY'] = environ.get('JWT_SECRET')
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(hours=1)
api = Api(app=app)
conexion = SQLAlchemy(app=app)
JWTManager(app=app)


class Usuario(conexion.Model):
    id = Column(type_= types.Integer, primary_key=True, autoincrement=True)
    nombre = Column(type_=types.String(length=100), nullable=False)
    apellido = Column(type_=types.String(length=100), nullable=False)
    correo = Column(type_=types.String(length=100), nullable=True, unique=True)
    password = Column(type_=types.Text)
    createdAt = Column(type_=types.DateTime, default = datetime.now(), name='created_at')

    __tablename__ = 'usuarios'


class Actividad(conexion.Model):
    id = Column(type_= types.Integer, primary_key=True, autoincrement=True)
    nombre = Column(type_=types.Text, nullable=False)
    descripcion = Column(type_=types.Text, nullable=False)
    habilitado = Column(type_=types.Boolean, default= True)
    fecha = Column(type_=types.DateTime)
    usuarioId = Column(ForeignKey(column='usuarios.id'), type_=types.Integer, nullable=False, name='usuario_id')

    __tablename__ = 'actividades'


class ActividadDto(SQLAlchemyAutoSchema):
    class Meta:
        model = Actividad

class RegistroDto(SQLAlchemyAutoSchema):
    class Meta:
        model = Usuario

class LoginDto(Schema):
    correo = fields.Email(required=True, error_messages = {'required': 'Este campo es requerido'})
    password = fields.Str(required=True, error_messages= { 'required': 'Este campo es requerido'})

class OlvidePasswordDto(Schema):
    correo = fields.Email(required=True)

class ReseteoPasswordDto(Schema):
    password = fields.Str(required=True)

class ActividadesController(Resource):
    @jwt_required()
    def post(self):
        usuarioId = get_jwt_identity()
        data = request.get_json()
        dto = ActividadDto()
        try:
            data_serializada = dto.load(data)
            nueva_actividad = Actividad(**data_serializada, usuarioId=usuarioId)
            conexion.session.add(nueva_actividad)
            conexion.session.commit()
            respuesta = dto.dump(nueva_actividad)

            return {
                'message': 'Actividad agregada exitosamente',
                'content': respuesta
            }, 201
        except Exception as e:
            return {
                'message': 'Error al crear la actividad',
                'content': e.args
            }, 400

    @jwt_required()
    def get(self):
        usuarioId = get_jwt_identity()
        actividades = conexion.session.query(Actividad).filter_by(usuarioId = usuarioId).all()
        dto = ActividadDto()
        respuesta = dto.dump(actividades, many=True)
        return {
            'content': respuesta
        }

class RegistroUsuarioController(Resource):
    def post(self):
        data = request.get_json()
        dto = RegistroDto()
        try:
            data_serializada = dto.load(data)
            password = bytes(data_serializada.get('password'),'utf-8')
            salt = gensalt(10)
            hash_password = hashpw(password, salt)
            print(str(hash_password))

            del data_serializada['password']

            nuevo_usuario = Usuario(**data_serializada, password=hash_password.decode('utf-8'))
            conexion.session.add(nuevo_usuario)
            conexion.session.commit()

            return {
                'message': 'Usuario registrado exitosamente'
            }, 201
        except Exception as e:
            return {
                'message': 'Error al crear el usuario',
                'content': e.args
            }, 400

class LoginController(Resource):
    def post(self):
        dto = LoginDto()
        try:
            data = request.get_json()
            data_serializada = dto.load(data)
            print(data_serializada)
            usuario:Usuario | None = conexion.session.query(Usuario).filter_by(correo= data_serializada.get('correo')).first()

            if usuario is None:
                raise Exception('El usuario no existe')
            
            password = bytes(usuario.password,'utf-8')
            password_por_confirmar = bytes(data_serializada.get('password'), 'utf-8')
            resultado = checkpw(password_por_confirmar, password)
            print(resultado)

            if resultado is False:
                raise Exception('El usuario no existe')
            token = create_access_token(identity=usuario.id)

            return {
                'content': token
            }
        except Exception as e:
            return {
                'message': 'Error al hacer el login',
                'content': e.args
            }

class OlvidePasswordController(Resource):
    def post(self):
        try:
            dto = OlvidePasswordDto()
            data= dto.load(request.get_json())
            olvide_password(data.get('correo'))

            return {
                'message': 'Correo enviado exitosamente'
            }
        except Exception as e:
            return {
                'message': 'Informacion incorrecta',
                'content': e.args
            }

class ReseteoPasswordController(Resource):
    def post(self):
        try:
            dto = ReseteoPasswordDto()
            data = dto.load(request.get_json())
            query_params = request.args # obtenemos los query params
            token = query_params.get('token')
            fernet = Fernet(environ.get('FERNET_KEY'))
            correo = fernet.decrypt(bytes(token,'utf-8')).decode('utf-8')

            usuario = conexion.session.query(Usuario).filter_by(correo= correo).first()
            if usuario is None:
                raise Exception('El usuario no existe')
            
            salt = gensalt(10)
            nueva_password = hashpw(bytes(data.get('password'),'utf-8'), salt).decode('utf-8')
            usuario.password = nueva_password
            conexion.session.commit()
            print(query_params)
            return {
                'message':'Contraseña cambiada exitosamente'
            }


        except Exception as e:
            return {
                'message': 'Error al resetear la contraseña',
                'cotent': e.args
            }

@app.before_first_request
def inicializacion():
    conexion.create_all()

api.add_resource(ActividadesController, '/actividades')
api.add_resource(RegistroUsuarioController, '/registro')
api.add_resource(LoginController, '/login')
api.add_resource(OlvidePasswordController, '/olvide-password')
api.add_resource(ReseteoPasswordController, '/resetear-password')

if __name__ =='__main__':
    app.run(debug=True)