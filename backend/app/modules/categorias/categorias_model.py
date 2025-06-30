from ...database.accesoBD import OperarBD

class CategoriaModel:

    def __init__(self, id: int=0, nombre: str=""):
        self.id = id
        self.nombre = nombre

    def serializar(self) -> dict:
        return {
            "id" : self.id,
            "nombre" : self.nombre
        }
    
    @staticmethod
    def deserializar(data: dict) -> 'CategoriaModel':
        return CategoriaModel(
            id = data['id'],
            nombre = data['nombre']
        )
    
    @staticmethod
    def verificar_existencia(data: dict) -> dict:
        #verifica que los datos de data coinidan con un registro de la BD (todos los campos)
        #return: {} si esta bien {error} si esta mal
        categoria_bd = CategoriaModel(data['id']).get_one()
        if not categoria_bd:
            return {'estado':'error', 'mensaje': 'La categoria recibida no existe en la base de datos'}
        if categoria_bd['nombre'] != data['nombre']:
            return {'estado':'error', 'mensaje': 'Datos de la categoria inconsistentes con la base de datos'}
        return {}

    #----Metodo estatico para obtener una lista de las categoras
    @staticmethod
    def get_all() -> list[dict]:
       return OperarBD.obtenerReg("SELECT * FROM CATEGORIAS")
    
    #----Metodo estatico para obtener una categoria
    def get_one(self) -> dict:
        registros = OperarBD.obtenerReg("SELECT * FROM CATEGORIAS WHERE id=%s",(self.id,))
        if registros:
            self.nombre = registros[0]['nombre']
            return registros[0] #Tomar el dict dentro de la lista. Sera siempre 1
        else:
            return {}

    #----Metodo para crear una categoria
    def create(self) -> bool | None:
        result = OperarBD.modifBD("INSERT INTO CATEGORIAS (nombre) VALUES (%s)",(self.nombre,))
        if result>0:
            self.id = result
            return True     #Se inserto en una tabla con PK auto-increment. Devolvio el nuevo id (no usado aqui) 
        else:
            return result   #result=True: Se inserto en una table con PK no auto-increment
                            #result=False: No se pudo insertar
                            #result=None: Alguna excepcion

    #----Metodo para modificar una categoria
    def update(self) -> bool | None:
        return OperarBD.modifBD("UPDATE CATEGORIAS SET nombre=%s WHERE id=%s",(self.nombre,self.id,))
    
    #----Metodo para eliminar una categoria
    @staticmethod
    def delete(id: int) -> bool | None:
        result = OperarBD.modifBD("DELETE FROM CATEGORIAS WHERE id=%s",(id,))
        if result==0:       #El motor de BD no pudo eliminar la categoria
            return False
        elif result==1:     #El motor de BD si pudo eliminar la categoria
            return True
        else:
            return None     #Alguna excepcion