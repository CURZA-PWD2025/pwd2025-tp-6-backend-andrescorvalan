from .articulos_model import ArticuloModel

class ArticuloController:

    @staticmethod
    def get_all() -> list[dict]:
        return ArticuloModel.get_all()
    
    @staticmethod
    def get_one(id: int) -> dict:
        articulo = ArticuloModel.get_one(id)
        return articulo
    
    @staticmethod
    def create(data: dict) -> dict:
        result = ArticuloModel().create(data)
        if result==True:
            return {'estado':'ok', 'mensaje': 'Articulo creado con exito'}
        elif result==False:
            return {'estado':'error', 'mensaje': 'No se pudo crear el articulo'}
        else:
            return {'estado':'exception', 'mensaje': 'No se pudo insertar el articulo en la BD por una excepcion'}

    @staticmethod
    def update(data: dict) -> dict:
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

