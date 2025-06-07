from .categorias_controller import CategoriaController
from flask import jsonify, request, Blueprint

categoria_bp = Blueprint("categorias",__name__)

#----Obtener todos las categorias
@categoria_bp.route("/categorias")
def get_all() -> dict:
    try:
        categorias = CategoriaController.get_all()
        if categorias:
            data = {
                "mensaje": "bien",
                "datos": categorias
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

#----Obtener una categoria
@categoria_bp.route("/categorias/<int:id>")
def get_one(id: int) -> dict:
    try:
        categoria = CategoriaController.get_one(id)
        if categoria:
            return jsonify(categoria), 200
        else:
            return jsonify({'mensaje': 'no se encontro la categoria'}), 404
    except Exception as una_execpcion:
        return jsonify({'mensaje': f"error {str(una_execpcion)}"}), 500
    
#----Crear una categoria
@categoria_bp.route("/categorias/", methods = ["POST"])
def create() -> dict:
    try:
        data = request.get_json()
        #controlar que se reciban datos
        if not data:
            return jsonify({'estado': 'error', 'mensaje': 'Petición no valida'}), 400

        dict_categ = CategoriaController.create(data)
        if dict_categ['estado']=='ok':
            return  jsonify(dict_categ), 201
        else: #dict_categ['estado']=='error' or dict_categ['estado']=='exception':
            return  jsonify(dict_categ), 500
    except Exception as una_execpcion:
        return jsonify({'estado': 'exception', 'mensaje': f"Exception en la ruta:{str(una_execpcion)}"}), 500
    
#----Modficar una categoria
@categoria_bp.route("/categorias/<int:id>", methods = ["PUT"])
def update(id: int) -> dict:
    try:
        data = request.get_json()
        #controlar que se reciban datos
        if not data:
            return jsonify({'estado': 'error', 'mensaje': 'Petición no valida'}), 400
        #controlar que el id de la url coincida con el de data
        if 'id' in data and data['id'] != id: 
            return jsonify({'estado': 'error', 'mensaje': 'El id en la URL no coincide con el id de los datos recibidos'}), 400
        
        data['id'] = id     #por si el id no esta en data

        dict_categ = CategoriaController.update(data)
        if dict_categ['estado']=='ok':
            return  jsonify(dict_categ), 200
        else: #dict_categ['estado']=='error' or dict_categ['estado']=='exception':
            return  jsonify(dict_categ), 500
    except Exception as una_execpcion:
        return jsonify({'estado': 'exception', 'mensaje': f"Exception en la ruta:{str(una_execpcion)}"}), 500

#----Eliminar una categoria
@categoria_bp.route("/categorias/<int:id>", methods = ["DELETE"])
def delete(id: int) -> dict:
    try:

        dict_categ = CategoriaController.delete(id)
        if dict_categ['estado']=='ok':
            return  jsonify(dict_categ), 200
        else: #dict_categ['estado']=='error' or dict_categ['estado']=='exception':
            return  jsonify(dict_categ), 500
    except Exception as una_execpcion:
        return jsonify({'estado': 'exception', 'mensaje': f"Exception en la ruta:{str(una_execpcion)}"}), 500