from .categorias_model import CategoriaModel

class CategoriaController:
    
    @staticmethod
    def get_all() -> list[dict]:
        return CategoriaModel.get_all()
    
    @staticmethod
    def get_one(id: int) -> dict:
        return CategoriaModel.get_one(id)

    @staticmethod
    def create(data: dict) -> dict:
        result = CategoriaModel().create(data)
        if result==True:
            return {'estado':'ok', 'mensaje': 'Categoria creada con exito'}
        elif result==False:
            return {'estado':'error', 'mensaje': 'No se pudo crear la categoria'}
        else:
            return {'estado':'exception', 'mensaje': 'No se pudo insertar la categoria en la BD por una excepción'}

    @staticmethod
    def update(data: dict) -> dict:
        result = CategoriaModel().update(data)
        if result==True:
            return {'estado':'ok', 'mensaje': 'Categoria actualizada con exito'}
        elif result==False:
            return {'estado':'error', 'mensaje': 'No se pudo actualizar la categoria'}
        else:
            return {'estado':'exception', 'mensaje': 'No se pudo actualizar la categoria en la BD por una excepción'}

    @staticmethod
    def delete(id: int) -> dict:
        result = CategoriaModel().delete(id)
        if result==True:
            return {'estado':'ok', 'mensaje': 'Categoria eliminada con exito'}
        elif result==False:
            return {'estado':'error', 'mensaje': 'No se pudo eliminar la categoria'}
        else:
            return {'estado':'exception', 'mensaje': 'No se pudo eliminar la categoria en la BD por una excepción'}

