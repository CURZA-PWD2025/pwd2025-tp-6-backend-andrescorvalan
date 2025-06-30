from .proveedores_controller import ProveedorController
from flask import jsonify, request, Blueprint

proveedor_bp = Blueprint("proveedores",__name__)

#----Obtener todos los proveedores
@proveedor_bp.route("/proveedores/")
def get_all() -> dict:
    try:
        proveedores = ProveedorController.get_all()
        if proveedores:
            #data = {
            #    "mensaje": "bien",
            #    "datos": proveedores
            #}
            code = 200
        else:
            #data = {
            #    "mensaje": "vacio",
            #    "datos": []
            #}
            code = 404
        return jsonify(proveedores), code
    except Exception as una_execpcion:
        return jsonify({'mensaje': f"error {str(una_execpcion)}"}), 500

#----Obtener un proveedor
@proveedor_bp.route("/proveedores/<int:id>")
def get_one(id: int) -> dict:
    try:
        proveedores = ProveedorController.get_one(id)
        if proveedores:
            return jsonify(proveedores), 200
        else:
            return jsonify({'mensaje': 'no se encontro el proveedor'}), 404
    except Exception as una_execpcion:
        return jsonify({'mensaje': f"error {str(una_execpcion)}"}), 500
    
#----Crear un proveedor
@proveedor_bp.route("/proveedores/", methods = ["POST"])
def create() -> dict:
    try:
        data = request.get_json()
        if not data:
            return jsonify({'estado': 'error', 'mensaje': 'Peticion no valida'}), 400
        dict_prov = ProveedorController.create(data)
        if dict_prov['estado']=='ok':
            return  jsonify(dict_prov), 201
        else: #dict_prov['estado']=='error' or dict_prov['estado']=='exception':
            return  jsonify(dict_prov), 500
    except Exception as una_execpcion:
        return jsonify({'estado': 'exception', 'mensaje': f"Exception en la ruta:{str(una_execpcion)}"}), 500

#----Modficar un proveedor
@proveedor_bp.route("/proveedores/<int:id>", methods = ["PUT"])
def update(id: int) -> dict:
    try:
        data = request.get_json()
        if not data:
            return jsonify({'estado': 'error', 'mensaje': 'Peticion no valida'}), 400
        #controlar que el id de la url coincida con el de data
        if 'id' in data and data['id'] != id: 
            return jsonify({'estado': 'error', 'mensaje': 'El id en la URL no coincide con el id de los datos recibidos'}), 400
        
        data['id'] = id     #por si el id no esta en data

        dict_prov = ProveedorController.update(data)
        if dict_prov['estado']=='ok':
            return  jsonify(dict_prov), 200
        else: #dict_prov['estado']=='error' or dict_prov['estado']=='exception':
            return  jsonify(dict_prov), 500
    except Exception as una_execpcion:
        return jsonify({'estado': 'exception', 'mensaje': f"Exception en la ruta:{str(una_execpcion)}"}), 500
    
#----Eliminar un proveedor
@proveedor_bp.route("/proveedores/<int:id>", methods = ["DELETE"])
def delete(id: int) -> dict:
    try:
        dict_prov = ProveedorController.delete(id)
        if dict_prov['estado']=='ok':
            return  jsonify(dict_prov), 200
        else: #dict_prov['estado']=='error' or dict_prov['estado']=='exception':
            return  jsonify(dict_prov), 500
    except Exception as una_execpcion:
        return jsonify({'estado': 'exception', 'mensaje': f"Exception en la ruta:{str(una_execpcion)}"}), 500