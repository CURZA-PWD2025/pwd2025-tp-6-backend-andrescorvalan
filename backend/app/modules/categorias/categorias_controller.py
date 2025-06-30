from .categorias_model import CategoriaModel

class CategoriaController:
    
    @staticmethod
    def get_all() -> list[dict]:
        return CategoriaModel.get_all()
    
    @staticmethod
    def get_one(id: int) -> dict:
        return CategoriaModel(id = id).get_one()

    @staticmethod
    def create(data: dict) -> dict:
        categoria =  CategoriaModel(nombre = data['nombre'])
        result = categoria.create()
        if result == True:
            return {'estado':'ok', 'mensaje': 'Categoria creada con exito', 'objeto': categoria.serializar()}
        elif result == False:
            return {'estado':'error', 'mensaje': 'No se pudo crear la categoria'}
        else:
            return {'estado':'exception', 'mensaje': 'No se pudo insertar la categoria en la BD por una excepción'}

    @staticmethod
    def update(data: dict) -> dict:
        categoria = CategoriaModel(
            id = data['id'],
            nombre = data['nombre']
        )
        result = categoria.update()
        if result is None:
             return {'estado':'exception', 'mensaje': 'No se pudo actualizar la categoria en la BD por una excepción'}
        if result==0:
            return {'estado':'ok', 'mensaje': 'Exito, aunque no se modifico nada de la categoria','objeto': categoria.serializar()}
        return {'estado':'ok', 'mensaje': 'Exito, se modifico la categoria','objeto': categoria.serializar()}

    @staticmethod
    def delete(id: int) -> dict:
        result = CategoriaModel.delete(id)
        if result==True:
            return {'estado':'ok', 'mensaje': 'Categoria eliminada con exito'}
        elif result==False:
            return {'estado':'error', 'mensaje': 'No se encontro la categoria a eliminar'}
        else:
            return {'estado':'exception', 'mensaje': 'No se pudo eliminar la categoria en la BD por una excepción'}

