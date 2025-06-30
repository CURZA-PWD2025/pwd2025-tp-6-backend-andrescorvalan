from ...database.accesoBD import OperarBD

class MarcaModel:

    def __init__(self, id: int=0, nombre: str=""):
        self.id = id
        self.nombre = nombre

    def serializar(self) -> dict:
        return {
            "id" : self.id,
            "nombre" : self.nombre
        }
    
    @staticmethod
    def deserializar(data: dict) -> 'MarcaModel':
        return MarcaModel(
            id = data['id'],
            nombre = data['nombre'],
        )
    
    @staticmethod
    def verificar_existencia(data: dict) -> dict:
        #verifica que los datos de data coinidan con un registro de la BD (todos los campos)
        #return: {} si esta bien {errores} si esta mal
        marca_bd = MarcaModel(data['id']).get_one()
        if not marca_bd:
            return {'estado':'error', 'mensaje': 'La marca recibida no existe en la base de datos'}
        if marca_bd['nombre'] != data['nombre']:
            return {'estado':'error', 'mensaje': 'Datos de la marca inconsistentes con la base de datos'}
        return {}

    #----Metodo estatico para obtener una lista de las marcas
    @staticmethod
    def get_all() -> list[dict]:
       return OperarBD.obtenerReg("SELECT * FROM MARCAS")
    
    #----Metodo estatico para obtener una marca
    def get_one(self) -> dict:
        registros = OperarBD.obtenerReg("SELECT * FROM MARCAS WHERE id=%s",(self.id,)) #Siempre sera 0 o 1 registro
        if registros:
            self.nombre = registros[0]['nombre']
            return registros[0] 
        else:
            return {}
        
    #----Metodo para crear una marca
    def create(self) -> bool | None:
        result = OperarBD.modifBD("INSERT INTO MARCAS (nombre) VALUES (%s)",(self.nombre,))
        if result>0:
            self.id = result
            return True     #Se inserto en una tabla con PK auto-increment. Devolvio el nuevo id
        else:
            return result   #result=True: Se inserto en una table con PK no auto-increment
                            #result=False: No se pudo insertar
                            #result=None: Alguna excepcion
   
    #----Metodo para modificar una marca
    def update(self) -> bool | None:
        return OperarBD.modifBD("UPDATE MARCAS SET nombre=%s WHERE id=%s",(self.nombre,self.id,))

    #----Metodo para eliminar un mara
    @staticmethod
    def delete(id: int) -> bool | None:
        result = OperarBD.modifBD("DELETE FROM MARCAS WHERE id=%s",(id,))
        if result==0:       #El motor de BD no pudo eliminar la marca
            return False
        elif result==1:     #El motor de BD si pudo eliminar la marca
            return True
        else:
            return None     #Alguna excepcion