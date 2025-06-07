from .marcas_model import MarcaModel

class MarcaController:
    
    @staticmethod
    def get_all() -> list[dict]:
        return MarcaModel.get_all()
    
    @staticmethod
    def get_one(id: int) -> dict:
        return MarcaModel.get_one(id)
    
    @staticmethod
    def create(data: dict) -> dict:
        result = MarcaModel().create(data)
        if result==True:
            return {'estado':'ok', 'mensaje': 'Marca creada con exito'}
        elif result==False:
            return {'estado':'error', 'mensaje': 'No se pudo crear la marca'}
        else:
            return {'estado':'exception', 'mensaje': 'No se pudo insertar la marca en la BD por una excepción'}

    @staticmethod
    def update(data: dict) -> dict:
        result = MarcaModel().update(data)
        if result==True:
            return {'estado':'ok', 'mensaje': 'Marca actualizada con exito'}
        elif result==False:
            return {'estado':'error', 'mensaje': 'No se pudo actualizar la marca'}
        else:
            return {'estado':'exception', 'mensaje': 'No se pudo actualizar la marca en la BD por una excepción'}

    @staticmethod
    def delete(id: int) -> dict:
        result = MarcaModel().delete(id)
        if result==True:
            return {'estado':'ok', 'mensaje': 'Marca eliminada con exito'}
        elif result==False:
            return {'estado':'error', 'mensaje': 'No se pudo eliminar la marca'}
        else:
            return {'estado':'exception', 'mensaje': 'No se pudo eliminar la marca en la BD por una excepción'}

