from .articulos_model import ArticuloModel
from ..marcas.marcas_model import MarcaModel
from ..proveedores.proveedores_model import ProveedorModel
from ..categorias.categorias_model import CategoriaModel

class ArticuloController:

    @staticmethod
    def get_all() -> list[dict]:
        return ArticuloModel.get_all()
    
    @staticmethod
    def get_one(id: int) -> dict:
        return  ArticuloModel(id = id).get_one()

    @staticmethod
    def verificar_data(data: dict) -> dict:
        #return: {} si esta bien {error} si esta mal
        if  data.get('descripcion') is None or \
            data.get('precio') is None or \
            data.get('stock') is None or \
            data.get('marca') is None or \
            data.get('categorias') is None or \
            data.get('proveedor') is None:
            return {'estado':'error', 'mensaje': 'Se recibieron datos del articulo incompletos'}
        marca_data = data['marca']
        if  marca_data.get('id') is None or \
            marca_data.get('nombre') is None:
            return {'estado':'error', 'mensaje': 'Se recibieron datos de la marca incompletos'}
        proveedor_data = data['proveedor']
        if  proveedor_data.get('id') is None or \
            proveedor_data.get('nombre') is None:
            return {'estado':'error', 'mensaje': 'Se recibieron datos del proveedor incompletos'}
        categorias_data = data['categorias']
        for cat_data in categorias_data:
            if  cat_data.get('id') is None or \
                cat_data.get('nombre') is None:
                return {'estado':'error', 'mensaje': 'Se recibieron datos de una categoria incompletos'}
        return {}

    @staticmethod
    def create(data: dict) -> dict:
        #validar data
        data_err = ArticuloController.verificar_data(data)
        if data_err:
            return data_err
        #validar existencia de la marca
        marca_err = MarcaModel.verificar_existencia(data['marca'])
        if marca_err:
            return marca_err
        #validar existencia del proveedor
        proveedor_err = ProveedorModel.verificar_existencia(data['proveedor'])
        if proveedor_err:
            return proveedor_err
        #validar existencia de las categorias
        categorias = []
        for catagoria_data in data['categorias']:
            categoria_err = CategoriaModel.verificar_existencia(catagoria_data)
            if categoria_err:
                return categoria_err
            categorias.append(CategoriaModel.deserializar(catagoria_data))
      
        #Crear el objeto articulo
        nuevo_articulo = ArticuloModel(
            descripcion = data['descripcion'],
            precio = data['precio'],
            stock = data['stock'],
            marca = MarcaModel.deserializar(data['marca']),
            proveedor = ProveedorModel.deserializar(data['proveedor']),
            categorias = categorias
        )
        
        #Crear en la BD
        result = nuevo_articulo.create()
        if result==True:
            return {'estado':'ok', 'mensaje': 'Articulo creado con exito'}
        elif result==False:
            return {'estado':'error', 'mensaje': 'No se pudo crear el articulo'}
        else:
            return {'estado':'exception', 'mensaje': 'No se pudo insertar el articulo en la base de datos por una excepcion'}

    @staticmethod
    def update(data: dict) -> dict:
        #verificar que se reciba un id y que exista un articulo con ese id
        if data.get('id') is None:
            return {'estado':'error', 'mensaje': 'No se recibió el ID del articulo'}
        articulo_bd = ArticuloModel.get_one(data['id'])
        if not articulo_bd:
            return {'estado':'error', 'mensaje': 'El articulo recibido no esta en la BD'}
        #validar data
        data_err = ArticuloController.verificar_data(data)
        if data_err:
            return data_err
        #validar existencia de la marca
        marca_err = MarcaModel.verificar_existencia(data['marca'])
        if marca_err:
            return marca_err
        #validar existencia del proveedor
        proveedor_err = ProveedorModel.verificar_existencia(data['proveedor'])
        if proveedor_err:
            return proveedor_err
        #validar existencia de las categorias
        categorias = []
        for catagoria_data in data['categorias']:
            categoria_err = CategoriaModel.verificar_existencia(catagoria_data)
            if categoria_err:
                return categoria_err
            categorias.append(CategoriaModel.deserializar(catagoria_data))

        result = ArticuloModel().update(data)
        if result==True:
            return {'estado':'ok', 'mensaje': 'Articulo actualizado con exito'}
        elif result==False:
            return {'estado':'error', 'mensaje': 'No se pudo actualizar el articulo'}
        else:
            return {'estado':'exception', 'mensaje': 'No se pudo actualizar el articulo en la BD por una excepcion'}

    @staticmethod
    def delete(id: int) -> dict:
        result = ArticuloModel().delete(id = id)
        if result==True:
            return {'estado':'ok', 'mensaje': 'Articulo eliminado con exito'}
        elif result==False:
            return {'estado':'error', 'mensaje': 'No se pudo eliminar el articulo'}
        else:
            return {'estado':'exception', 'mensaje': 'No se pudo eliminar el articulo en la BD por una excepcion'}

