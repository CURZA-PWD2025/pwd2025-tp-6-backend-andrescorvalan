from .articulos_controller import ArticuloController
from flask import jsonify, request, Blueprint

articulo_bp = Blueprint("articulos",__name__)

#----Obtener todos los articulos
@articulo_bp.route("/articulos")
def get_all() -> dict:
    try:
        articulos = ArticuloController.get_all()
        if articulos:
            data = {
                "mensaje": "bien",
                "datos": articulos
            }
            code = 200
        else:
            data = {
                "mensaje": "vacio",
                "datos": []
            }
            code = 404
        return jsonify(data), code
    except Exception as una_execpcion:
        return jsonify({'mensaje': f"error {str(una_execpcion)}"}), 500
    
#----Obtener un articulo
@articulo_bp.route("/articulos/<int:id>")
def get_one(id: int) -> dict:
    try:
        articulo = ArticuloController.get_one(id)
        if articulo:
            return jsonify(articulo), 200
        else:
            return jsonify({'mensaje': 'no se encontro el articulo'}), 404
    except Exception as una_execpcion:
        return jsonify({'mensaje': f"error {str(una_execpcion)}"}), 500
    
#----Crear un articulo
@articulo_bp.route("/articulos/", methods = ["POST"])
def create() -> dict:
    try:
        data = request.get_json()
        if not data:
            return jsonify({'estado': 'error', 'mensaje': 'Peticion no valida'}), 400
      
        dict_artic = ArticuloController.create(data)
        if dict_artic['estado']=='ok':
            return  jsonify(dict_artic), 201
        else: #dict_artic['estado']=='error' or dict_artic['estado']=='exception':
            return  jsonify(dict_artic), 500
    except Exception as una_execpcion:
        return jsonify({'estado': 'exception', 'mensaje': f"Exception en la ruta:{str(una_execpcion)}"}), 500
    
#----Modficar un articulo
@articulo_bp.route("/articulos/<int:id>", methods = ["PUT"])
def update(id: int) -> dict:
    try:
        data = request.get_json()
        if not data:
            return jsonify({'estado': 'error', 'mensaje': 'Peticion no valida'}), 400
        #controlar que el id de la url coincida con el de data
        if 'id' in data and data['id'] != id: 
            return jsonify({'estado': 'error', 'mensaje': 'El id en la URL no coincide con el id de los datos recibidos'}), 400
        data['id'] = id     #por si el id no esta en data

        dict_artic = ArticuloController.update(data)
        if dict_artic['estado']=='ok':
            return  jsonify(dict_artic), 200
        else: #dict_artic['estado']=='error' or dict_artic['estado']=='exception':
            return  jsonify(dict_artic), 500
    except Exception as una_execpcion:
        return jsonify({'estado': 'exception', 'mensaje': f"Exception en la ruta:{str(una_execpcion)}"}), 500
    
#----Eliminar un articulo
@articulo_bp.route("/articulos/<int:id>", methods = ["DELETE"])
def delete(id: int) -> dict:
    try:
        dict_artic = ArticuloController.delete(id)
        if dict_artic['estado']=='ok':
            return  jsonify(dict_artic), 200
        else: #dict_artic['estado']=='error' or dict_artic['estado']=='exception':
            return  jsonify(dict_artic), 500
    except Exception as una_execpcion:
        return jsonify({'estado': 'exception', 'mensaje': f"Exception en la ruta:{str(una_execpcion)}"}), 500