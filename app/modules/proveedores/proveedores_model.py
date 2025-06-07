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

    #----Metodo estatico para obtener una lista de los proveedores
    @staticmethod
    def get_all() -> list[dict]:
        return OperarBD.obtenerReg("SELECT * FROM PROVEEDORES")
        
    #----Metodo estatico para obtener un proveedor
    @staticmethod
    def get_one(id: int) -> dict:
        registros = OperarBD.obtenerReg("SELECT * FROM PROVEEDORES WHERE id=%s",(id,))
        if registros:
            return registros[0] #Tomar el dict dentro de la lista
        else:
            return {}
        
    #----Metodo para crear un proveedor
    def create(self, data: dict) -> bool | None:
        result = OperarBD.modifBD("INSERT INTO PROVEEDORES (nombre, telefono, direccion, email) VALUES (%s, %s, %s, %s)",
                                (data['nombre'],data['telefono'],data['direccion'],data['email']))
        #Analisis del resultado
        if result>0:
            return True     #Se inserto en una tabla con PK auto-increment. Devolvio el nuevo id (no usado aqui) 
        else:
            return result   #result=True: Se inserto en una table con PK no auto-increment
                            #result=False: No se pudo insertar
                            #result=None: Alguna excepcion

    #----Metodo para modificar un proveedor
    def update(self, data: dict) -> bool | None:
        result = OperarBD.modifBD("UPDATE PROVEEDORES SET nombre=%s, telefono=%s, direccion=%s, email=%s WHERE id=%s",
                                (data['nombre'],data['telefono'],data['direccion'],data['email'],data['id'],))

        if result==0:       #El motor de BD no pudo actualizar el proveedor
            return False
        elif result==1:     #El motor de BD si pudo actualizar el proveedor
            return True
        else:
            return None     #Alguna excepcion

    #----Metodo para eliminar un proveedor
    def delete(self, id: int) -> bool | None:
        result = OperarBD.modifBD("DELETE FROM PROVEEDORES WHERE id=%s",(id,))
        if result==0:       #El motor de BD no pudo eliminar el proveedor
            return False
        elif result==1:     #El motor de BD si pudo eliminar el proveedor
             return True
        else:
            return None     #Alguna excepcion