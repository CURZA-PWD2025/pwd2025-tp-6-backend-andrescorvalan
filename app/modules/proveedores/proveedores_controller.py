from .proveedores_model import ProveedorModel

class ProveedorController:
    
    @staticmethod
    def get_all() -> list[dict]:
        return ProveedorModel.get_all()
    
    @staticmethod
    def get_one(id: int) -> dict:
        return ProveedorModel.get_one(id)
    
    @staticmethod
    def create(data: dict) -> dict:
        result = ProveedorModel().create(data)
        if result==True:
            return {'estado':'ok', 'mensaje': 'Proveedor creado con exito'}
        elif result==False:
            return {'estado':'error', 'mensaje': 'No se pudo crear el proveedor'}
        else:
            return {'estado':'exception', 'mensaje': 'No se pudo insertar el proveedor en la BD por una excepción'}

    @staticmethod
    def update(data: dict) -> dict:
        result = ProveedorModel().update(data)
        if result==True:
            return {'estado':'ok', 'mensaje': 'Proveedor actualizado con exito'}
        elif result==False:
            return {'estado':'error', 'mensaje': 'No se pudo actualizar el proveedor'}
        else:
            return {'estado':'exception', 'mensaje': 'No se pudo actualizar el proveedor en la BD por una excepción'}

    @staticmethod
    def delete(id: int) -> dict:
        result = ProveedorModel().delete(id)
        if result==True:
            return {'estado':'ok', 'mensaje': 'Proveedor eliminado con exito'}
        elif result==False:
            return {'estado':'error', 'mensaje': 'No se pudo eliminar el proveedor'}
        else:
            return {'estado':'exception', 'mensaje': 'No se pudo eliminar el proveedor en la BD por una excepción'}

