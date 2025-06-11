from ...database.accesoBD import OperarBD,TransaccionBD
from ..marcas.marcas_model import MarcaModel
from ..proveedores.proveedores_model import ProveedorModel
from ..categorias.categorias_model import CategoriaModel

class ArticuloModel():
    
    def __init__(self, id: int=0, descripcion: str="", precio: float=0.0, stock: int=0, 
                 marca: MarcaModel=None, 
                 proveedor: ProveedorModel=None, 
                 categorias: list[CategoriaModel] = None):
        self.id = id
        self.descripcion = descripcion
        self.precio = precio
        self.stock = stock
        self.marca = marca
        self.proveedor = proveedor
        self.categorias = categorias if categorias is not None else []
 
    def serializar(self):
        return {
            "id": self.id,
            "descripcion": self.descripcion,
            "precio": self.precio,
            "stock": self.stock,
            "marca": self.marca.serializar(),
            "proveedor": self.proveedor.serializar(),
            "categorias": [una_cat.serializar() for una_cat in self.categorias]
        }

    @staticmethod
    def deserializar(data: dict):
        #Control de existencia de los datos de marca, proveedor y lista de categorias
        #Igualmente se asume que data esta bien formado
        if data.get('marca') is None or data.get('proveedor') is None or data.get('categorias') is None or not isinstance(data['categorias'], list):
            raise ValueError("Valores no validos")
        
        categorias = []
        for una_cat in data['categorias']:
            categorias.append(CategoriaModel.deserializar(una_cat))
 
        return ArticuloModel(
            id = data['id'],
            descripcion = data['descripcion'], 
            precio = data['precio'], 
            stock = data['stock'],
            marca = MarcaModel.deserializar(data['marca']),
            proveedor = ProveedorModel.deserializar(data['proveedor']),
            categorias = categorias
        )
    
        #----Metodo estatico para obtener una lista de los articulos
    @staticmethod
    def get_all() -> list[dict]:

        listado = []
        articulos_bd = OperarBD.obtenerReg("SELECT * FROM ARTICULOS")
        for articulo_data in articulos_bd:
            
            marca_id = articulo_data['marca_id']
            articulo_data.pop('marca_id')
            articulo_data['marca'] = MarcaModel(marca_id).get_one()

            proveedor_id = articulo_data['proveedor_id']
            articulo_data.pop('proveedor_id')
            articulo_data['proveedor'] = ProveedorModel(proveedor_id).get_one()
            
            categorias_bd = OperarBD.obtenerReg("SELECT categoria_id FROM ARTICULOS_CATEGORIAS WHERE articulo_id=%s",(articulo_data['id'],))
            categorias = []
            for id_cat in categorias_bd:
                categorias.append(CategoriaModel(id_cat['categoria_id']).get_one())
            articulo_data['categorias'] = categorias

            listado.append(articulo_data)
        return listado 
  
    #----Metodo estatico para obtener un articulo
    @staticmethod
    def get_one(id: int) -> dict:
        
        articulo_bd = OperarBD.obtenerReg("SELECT * FROM ARTICULOS WHERE id=%s",(id,))
        if articulo_bd:
            articulo_data = articulo_bd[0]

            marca_id = articulo_data['marca_id']
            articulo_data.pop('marca_id')
            articulo_data['marca'] = MarcaModel(marca_id).get_one()

            proveedor_id = articulo_data['proveedor_id']
            articulo_data.pop('proveedor_id')
            articulo_data['proveedor'] = ProveedorModel(proveedor_id).get_one()

            categorias_bd = OperarBD.obtenerReg("SELECT categoria_id FROM ARTICULOS_CATEGORIAS WHERE articulo_id=%s",(articulo_data['id'],))
            categorias = []
            for id_cat in categorias_bd:
                categorias.append(CategoriaModel(id_cat['categoria_id']).get_one())
            articulo_data['categorias'] = categorias
            return articulo_data 
        else:
            return {}

    #----Metodo para crear un articulo
    def create(self) -> bool | None:
        #se usa una transaccion porque se deben realizar varias escrituras (todas o ninguna)
        transaccion = None
        try:
            transaccion = TransaccionBD()
            transaccion.iniciar_transaccion()
            #Insertar el articulo
            if not transaccion.operacionBD(
                "INSERT INTO ARTICULOS (descripcion, precio, stock, marca_id, proveedor_id) VALUES (%s, %s, %s, %s, %s)",
                (self.descripcion, self.precio, self.stock, self.marca.id, self.proveedor.id,)):
                transaccion.revertir_transaccion()
                return False    #si hubo un error, salir con false
            self.id = transaccion.get_nuevo_id()
            #Insertar la relacion Articulos-Categorias
            for una_cat in self.categorias:
                if not transaccion.operacionBD(
                    "INSERT INTO ARTICULOS_CATEGORIAS (articulo_id,categoria_id) VALUES (%s, %s)",
                    (self.id, una_cat.id,)):
                    transaccion.revertir_transaccion()
                    return False    #si hubo un error, salir con false
            #Se inserto correctamente
            transaccion.confirmar_transaccion()
            return True
        except Exception as err:
            print(f"Error al crear el artículo: {err}")
            return None
        finally:
            if transaccion:
                transaccion.finalizar_transaccion()

    #----Metodo para modificar un articulo
    def update(self, data: dict) -> bool | None:
        transaccion = None
        try:
            transaccion = TransaccionBD()
            transaccion.iniciar_transaccion()
            #actualizar el articulo
            
            if not transaccion.operacionBD(
                "UPDATE ARTICULOS SET descripcion=%s, precio=%s, stock=%s, marca_id=%s, proveedor_id=%s WHERE id=%s",
                    (data['descripcion'],data['precio'],data['stock'],data['marca']['id'],data['proveedor']['id'],data['id'],)):
                
                transaccion.revertir_transaccion()
                return False
           
            #Eliminar las categorias anteriores
            if not transaccion.operacionBD("DELETE FROM ARTICULOS_CATEGORIAS WHERE articulo_id=%s",(data['id'],)):
                transaccion.revertir_transaccion()
                return False 
            
            #Agregar las categorias nuevas
            for una_cat in data['categorias']:
                if not transaccion.operacionBD("INSERT INTO ARTICULOS_CATEGORIAS (articulo_id,categoria_id) VALUES (%s, %s)",
                                                (data['id'], una_cat['id'],)):
                    transaccion.revertir_transaccion()
                    return False 
            #Se actualizo
            transaccion.confirmar_transaccion()
            return True     #El motor de BD pudo actualizar 
               
        except Exception as err:
            print(f"Error al actualizar el artículo: {err}")
            return None
        finally:
            if transaccion:
                transaccion.finalizar_transaccion()

    #----Metodo para eliminar un articulo
    def delete(self, id: int) -> bool | None:
        transaccion = None
        try:
            transaccion = TransaccionBD()
            transaccion.iniciar_transaccion()

            transaccion.operacionBD("DELETE FROM ARTICULOS_CATEGORIAS WHERE articulo_id=%s",(id,))
             
            if not transaccion.operacionBD("DELETE FROM ARTICULOS WHERE id=%s",(id,)):
                print(f"DEBUG: Fallo al borrar de ARTICULOS. rowcount era 0 o menos.")  
                transaccion.revertir_transaccion()
                return False 
            
            #Se borro
            transaccion.confirmar_transaccion()
            return True     #El motor de BD pudo eliminar 
        except Exception as err:
            print(f"Error al eliminar el artículo: {err}")
            return None
        finally:
            if transaccion:
                transaccion.finalizar_transaccion()
