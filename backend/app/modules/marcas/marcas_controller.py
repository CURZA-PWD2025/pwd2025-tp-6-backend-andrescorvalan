from .marcas_model import MarcaModel

class MarcaController:
    
    @staticmethod
    def get_all() -> list[dict]:
        return MarcaModel.get_all()
    
    @staticmethod
    def get_one(id: int) -> dict:
        return MarcaModel(id = id).get_one()
    
    @staticmethod
    def create(data: dict) -> dict:
        marca =  MarcaModel(nombre = data['nombre'])
        result = marca.create()
        if result == True: 
            return {'estado':'ok', 'mensaje': 'Marca creada con exito','objeto': marca.serializar()}
        elif result == False:
            return {'estado':'error', 'mensaje': 'No se pudo crear la marca'}
        else:
            return {'estado':'exception', 'mensaje': 'No se pudo insertar la marca en la BD por una excepción'}

    @staticmethod
    def update(data: dict) -> dict:
        marca = MarcaModel(
            id = data['id'],
            nombre = data['nombre']
        )
        result = marca.update()
        if result is None:
            return {'estado':'exception', 'mensaje': 'No se pudo actualizar la marca en la BD por una excepción'}
        if result==0:
            return {'estado':'ok', 'mensaje': 'Exito, aunque no se modifico nada de la marca','objeto': marca.serializar()}
        return {'estado':'ok', 'mensaje': 'Exito, se modifico la marca','objeto': marca.serializar()}
        
    @staticmethod
    def delete(id: int) -> dict:
        result = MarcaModel.delete(id)
        if result==True:
            return {'estado':'ok', 'mensaje': 'Marca eliminada con exito'}
        elif result==False:
            return {'estado':'error', 'mensaje': 'No se encontro la marca a eliminar'}
        else:
            return {'estado':'exception', 'mensaje': 'No se pudo eliminar la marca en la BD por una excepción'}