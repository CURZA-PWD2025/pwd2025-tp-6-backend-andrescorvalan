from ...database.accesoBD import OperarBD

class ProveedorModel:

    def __init__(self, id: int=0, nombre: str="", telefono: str="", direccion: str="", email: str=""):
        self.id = id
        self.nombre = nombre
        self.telefono = telefono
        self.direccion = direccion
        self.email = email

    def serializar(self) -> dict:
        return {
            'id' : self.id,
            'nombre' : self.nombre,
            'telefono' : self.telefono,
            'direccion' : self.direccion,
            'email' : self.email
        }

    @staticmethod
    def deserializar(data: dict) -> 'ProveedorModel':
        return ProveedorModel(
            id = data['id'],
            nombre = data['nombre'],
            telefono = data['telefono'],
            direccion =data['direccion'], 
            email = data['email']
        )
    @staticmethod
    def verificar_existencia(data: dict) -> dict:
        #verifica que los datos de data coinidan con un registro de la BD (todos los campos)
        #return: {} si esta bien {error} si esta mal
        proveedor_bd = ProveedorModel(data['id']).get_one()
        if not proveedor_bd:
            return {'estado':'error', 'mensaje': 'El proveedor recibida no existe en la base de datos'}
        if  proveedor_bd['nombre'] != data['nombre'] or \
            proveedor_bd['telefono'] != data['telefono'] or\
            proveedor_bd['direccion'] != data['direccion'] or\
            proveedor_bd['email'] != data['email']:
            return {'estado':'error', 'mensaje': 'Datos del proveedor inconsistentes con la base de datos'}
        return {}
    
    #----Metodo estatico para obtener una lista de los proveedores
    @staticmethod
    def get_all() -> list[dict]:
        return OperarBD.obtenerReg("SELECT * FROM PROVEEDORES")
        
    #----Metodo estatico para obtener un proveedor
    def get_one(self) -> dict:
        registros = OperarBD.obtenerReg("SELECT * FROM PROVEEDORES WHERE id=%s",(self.id,))
        if registros:
            return registros[0] #Tomar el dict dentro de la lista
        else:
            return {}
        
    #----Metodo para crear un proveedor
    def create(self) -> bool | None:
        result = OperarBD.modifBD("INSERT INTO PROVEEDORES (nombre, telefono, direccion, email) VALUES (%s, %s, %s, %s)",
                                (self.nombre,self.telefono,self.direccion,self.email))
        if result>0:
            return True     #Se inserto en una tabla con PK auto-increment. Devolvio el nuevo id (no usado aqui) 
        else:
            return result   #result=True: Se inserto en una table con PK no auto-increment
                            #result=False: No se pudo insertar
                            #result=None: Alguna excepcion
    
    #----Metodo para modificar un proveedor
    def update(self) -> bool | None:
        return OperarBD.modifBD("UPDATE PROVEEDORES SET nombre=%s, telefono=%s, direccion=%s, email=%s WHERE id=%s",
                                (self.nombre,self.telefono,self.direccion,self.email,self.id,))

    #----Metodo para eliminar un proveedor
    @staticmethod
    def delete(id: int) -> bool | None:
        result = OperarBD.modifBD("DELETE FROM PROVEEDORES WHERE id=%s",(id,))
        if result==0:       #El motor de BD no pudo eliminar el proveedor
            return False
        elif result==1:     #El motor de BD si pudo eliminar el proveedor
             return True
        else:
            return None     #Alguna excepcion