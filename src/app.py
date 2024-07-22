from flask import Flask, request, jsonify, Response
from flask_pymongo import PyMongo
from werkzeug.security import generate_password_hash, check_password_hash
from bson import json_util
from urllib.parse import quote_plus


username = "Juan"
password = "LzRJKwlcafsgSsLS"
cluster = "juan.tp5nqmq.mongodb.net"
database_name = "tu_database_name"

app = Flask(__name__)
app.config['MONGO_URI'] = f"mongodb+srv://Juan:LzRJKwlcafsgSsLS@juan.tp5nqmq.mongodb.net/tu_database_name?retryWrites=true&w=majority"
mongo = PyMongo(app)


@app.route('/usuarios', methods = ['POST'])
def crearusuario():
    nombreusuario = request.json['nombreusuario']
    contraseña = request.json['contraseña']
    correo = request.json['correo']

    if nombreusuario and contraseña and correo:
        contraseñacifrada = generate_password_hash(contraseña)
        id = str(mongo.db.usuarios.insert_one({
            'nombreusuario': nombreusuario,
            'correo': correo,
            'contraseña': contraseñacifrada
        }).inserted_id)

        response = {
            'id': str(id),
            'nombreusuario': nombreusuario,
            'contraseña': contraseñacifrada,
            'correo': correo
        }
        return response
    
    else:
        return not_found()

@app.route('/usuarios',methods=['GET'])
def obtener_usuarios():
    usuario = mongo.db.usuarios.find()
    respuesta = json_util.dumps(usuario)
    return Response(respuesta, mimetype='application/json')

@app.route('/usuarios/<nombreusuario>', methods=['GET'])
def obtener_usuario(nombreusuario):
    usuario = mongo.db.usuarios.find_one({'nombreusuario':nombreusuario})
    respuesta = json_util.dumps(usuario)
    return respuesta

@app.route('/usuarios/<nombreusuario>', methods=['DELETE'])
def eliminar_usuario(nombreusuario):
    mongo.db.usuarios.delete_one({'nombreusuario':nombreusuario})
    respuesta = jsonify({'mensaje':'El usuario con el nombre ' + nombreusuario + ' fue eliminado exitosamente'})
    return respuesta

@app.route('/usuarios/<nombreusuario>', methods=['PUT'])
def actualizar_usuario(nombreusuario):
    nombreusuario = request.json['nombreusuario']
    contraseña = request.json['contraseña']
    correo = request.json['correo']
    if nombreusuario and contraseña and correo:
        contraseña_cifrada = generate_password_hash(contraseña)
        mongo.db.usuarios.update_one({'nombreusuario':nombreusuario},{set: {
            'nombreusuario': nombreusuario,
            'correo': correo,
            'contraseña': contraseña_cifrada
        }})
        respuesta = jsonify({'mensaje':'El ususario con el nombre ' + nombreusuario + ' fue actualizado exitosamente'})
        return respuesta

@app.errorhandler(404)
def not_found(error=None):
    respuesta = jsonify({
        'message': 'Resource Not Found' + request.url,
        'status': 404
    })
    respuesta.status_code = 404
    return respuesta
    
    
if __name__ == '__main__':
    app.run(debug=True, port=5000)