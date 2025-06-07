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
    
    #----Metodo estatico para obtener una lista de las marcas
    @staticmethod
    def get_all() -> list[dict]:
       return OperarBD.obtenerReg("SELECT * FROM MARCAS")
    
    #----Metodo estatico para obtener una marca
    @staticmethod
    def get_one(id: int) -> dict:
        registros = OperarBD.obtenerReg("SELECT * FROM MARCAS WHERE id=%s",(id,))
        if registros:
            return registros[0] #Tomar el dict dentro de la lista
        else:
            return {}
   
    #----Metodo para crear una marca
    def create(self, data: dict) -> bool | None:
        result = OperarBD.modifBD("INSERT INTO MARCAS (nombre) VALUES (%s)",(data['nombre'],))
        #Analisis del resultado
        if result>0:
            return True     #Se inserto en una tabla con PK auto-increment. Devolvio el nuevo id (no usado aqui) 
        else:
            return result   #result=True: Se inserto en una table con PK no auto-increment
                            #result=False: No se pudo insertar
                            #result=None: Alguna excepcion

    #----Metodo para modificar una marca
    def update(self, data: dict) -> bool | None:
        result = OperarBD.modifBD("UPDATE MARCAS SET nombre=%s WHERE id=%s",(data['nombre'],data['id'],))
        if result==0:       #El motor de BD no pudo actualizar la marca
            return False
        elif result==1:     #El motor de BD si pudo actualizar la marca
            return True
        else:
            return None     #Alguna excepcion

    #----Metodo para eliminar un mara
    def delete(self, id: int) -> bool | None:
        result =  OperarBD.modifBD("DELETE FROM MARCAS WHERE id=%s",(id,))
        if result==0:       #El motor de BD no pudo eliminar la marca
            return False
        elif result==1:     #El motor de BD si pudo eliminar la marca
            return True
        else:
            return None     #Alguna excepcion