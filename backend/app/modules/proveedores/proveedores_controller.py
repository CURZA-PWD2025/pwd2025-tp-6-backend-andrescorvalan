from .proveedores_model import ProveedorModel

class ProveedorController:
    
    @staticmethod
    def get_all() -> list[dict]:
        return ProveedorModel.get_all()
    
    @staticmethod
    def get_one(id: int) -> dict:
        return ProveedorModel(id = id).get_one()
    
    @staticmethod
    def create(data: dict) -> dict:
        proveedor = ProveedorModel(
            nombre = data['nombre'],
            telefono = data['telefono'],
            direccion = data['direccion'],
            email = data['email'])
        result = proveedor.create()
        if result==True:
            return {'estado':'ok', 'mensaje': 'Proveedor creado con exito', 'objeto': proveedor.serializar()}
        elif result==False:
            return {'estado':'error', 'mensaje': 'No se pudo crear el proveedor'}
        else:
            return {'estado':'exception', 'mensaje': 'No se pudo insertar el proveedor en la BD por una excepción'}

    @staticmethod
    def update(data: dict) -> dict:
        proveedor = ProveedorModel(
            id = data['id'],
            nombre = data['nombre'],
            telefono = data['telefono'],
            direccion = data['direccion'],
            email = data['email'])
        result = proveedor.update()
        if result is None:
            return {'estado':'exception', 'mensaje': 'No se pudo actualizar el proveedor en la BD por una excepción'}

        if result==0:
            return {'estado':'ok', 'mensaje': 'Exito, aunque no se modifico nada del proveeodr','objeto': proveedor.serializar()}
        return {'estado':'ok', 'mensaje': 'Exito, se modifico el proveedor', 'objeto': proveedor.serializar()}
    

        if result==True:
            return {'estado':'ok', 'mensaje': 'Proveedor actualizado con exito', 'objeto': proveedor.serializar()}
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
            return {'estado':'error', 'mensaje': 'No se encontro el proveedor a eliminar'}
        else:
            return {'estado':'exception', 'mensaje': 'No se pudo eliminar el proveedor en la BD por una excepción'}