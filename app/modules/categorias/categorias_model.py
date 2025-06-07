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
    
    #----Metodo estatico para obtener una lista de las categoras
    @staticmethod
    def get_all() -> list[dict]:
       return OperarBD.obtenerReg("SELECT * FROM CATEGORIAS")
    
    #----Metodo estatico para obtener una categoria
    @staticmethod
    def get_one(id: int) -> dict:
        registros = OperarBD.obtenerReg("SELECT * FROM CATEGORIAS WHERE id=%s",(id,))
        if registros:
            return registros[0] #Tomar el dict dentro de la lista
        else:
            return {}

    #----Metodo para crear una categoria
    def create(self, data: dict) -> bool | None:
        result = OperarBD.modifBD("INSERT INTO CATEGORIAS (nombre) VALUES (%s)",(data['nombre'],))
        #Analisis del resultado
        if result>0:
            return True     #Se inserto en una tabla con PK auto-increment. Devolvio el nuevo id (no usado aqui) 
        else:
            return result   #result=True: Se inserto en una table con PK no auto-increment
                            #result=False: No se pudo insertar
                            #result=None: Alguna excepcion

    #----Metodo para modificar una categoria
    def update(self, data: dict) -> bool | None:
        result = OperarBD.modifBD("UPDATE CATEGORIAS SET nombre=%s WHERE id=%s",(data['nombre'],data['id'],))
        if result==0:       #El motor de BD no pudo actualizar la categoria
            return False
        elif result==1:     #El motor de BD si pudo actualizar la categoria
            return True
        else:
            return None     #Alguna excepcion
    
    #----Metodo para eliminar una categoria
    def delete(self, id: int) -> bool | None:
        result =  OperarBD.modifBD("DELETE FROM CATEGORIAS WHERE id=%s",(id,))
        if result==0:       #El motor de BD no pudo eliminar la categoria
            return False
        elif result==1:     #El motor de BD si pudo eliminar la categoria
            return True
        else:
            return None     #Alguna excepcion