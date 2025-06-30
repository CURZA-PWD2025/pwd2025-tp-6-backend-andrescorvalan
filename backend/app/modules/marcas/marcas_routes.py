from .marcas_controller import MarcaController
from flask import jsonify, request, Blueprint

marca_bp = Blueprint("marcas",__name__)

#----Obtener todos las marcas
@marca_bp.route("/marcas/")
def get_all() -> dict:
    try:
        marcas = MarcaController.get_all()
        if marcas:
            #data = {
            #    "mensaje": "bien",
            #    "datos": marcas
            #}
            code = 200
        else:
            #data = {
            #    "mensaje": "vacio",
            #    "datos": []
            #}
            code = 404
        return jsonify(marcas), code
    except Exception as una_execpcion:
        return jsonify({'mensaje': f"error {str(una_execpcion)}"}), 500
    
#----Obtener una marca
@marca_bp.route("/marcas/<int:id>")
def get_one(id: int) -> dict:
    try:
        marca = MarcaController.get_one(id)
        if marca:
            return jsonify(marca), 200
        else:
            return jsonify({'mensaje': 'no se encontro la marca'}), 404
    except Exception as una_execpcion:
        return jsonify({'mensaje': f"error {str(una_execpcion)}"}), 500
    
#----Crear una marca
@marca_bp.route("/marcas/", methods = ["POST"])
def create() -> dict:
    try:
        data = request.get_json()
        if not data:
            return jsonify({'estado': 'error', 'mensaje': 'Peticion no valida'}), 400
        dict_marca = MarcaController.create(data)
        if dict_marca['estado']=='ok':
            return  jsonify(dict_marca), 201
        
        else: #dict_marca['estado']=='error' or dict_marca['estado']=='exception':
            return  jsonify(dict_marca), 500
    except Exception as una_execpcion:
        return jsonify({'estado': 'exception', 'mensaje': f"Exception en la ruta:{str(una_execpcion)}"}), 500
    
#----Modficar una marca
@marca_bp.route("/marcas/<int:id>", methods = ["PUT"])
def update(id: int) -> dict:
    try:
        data = request.get_json()
        if not data:
            return jsonify({'estado': 'error', 'mensaje': 'Peticion no valida'}), 400
        #controlar que el id de la url coincida con el de data
        if 'id' in data and data['id'] != id: 
            return jsonify({'estado': 'error', 'mensaje': 'El id en la URL no coincide con el id de los datos recibidos'}), 400
        
        data['id'] = id     #por si el id no esta en data

        dict_marca = MarcaController.update(data)
        if dict_marca['estado']=='ok':
            return  jsonify(dict_marca), 200
        else: #dict_marca['estado']=='error' or dict_marca['estado']=='exception':
            return  jsonify(dict_marca), 500
    except Exception as una_execpcion:
        return jsonify({'estado': 'exception', 'mensaje': f"Exception en la ruta:{str(una_execpcion)}"}), 500
    
#----Eliminar una marca
@marca_bp.route("/marcas/<int:id>", methods = ["DELETE"])
def delete(id: int) -> dict:
    try:
        dict_marca = MarcaController.delete(id)
        if dict_marca['estado']=='ok':
            return  jsonify(dict_marca), 200
        else: #dict_marca['estado']=='error' or dict_marca['estado']=='exception':
            return  jsonify(dict_marca), 500
    except Exception as una_execpcion:
        return jsonify({'estado': 'exception', 'mensaje': f"Exception en la ruta:{str(una_execpcion)}"}), 500