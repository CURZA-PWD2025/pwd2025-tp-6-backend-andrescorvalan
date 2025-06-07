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
            id = data['id'], descripcion = data['descripcion'], precio = data['precio'], stock = data['stock'],
            marca = MarcaModel.deserializar(data['marca']),
            proveedor = ProveedorModel.deserializar(data['proveedor']),
            categorias = categorias
        )
    
    #----Metodo estatico para obtener una lista de los articulos
    @staticmethod
    def get_all() -> list[dict]:
        transaccion = None
        try:
            transaccion = TransaccionBD()
            transaccion.iniciar_transaccion()

            #Obtener todas las marcas y armar un index {id, dict}
            marcas = transaccion.obtenerReg("SELECT * FROM MARCAS")
            index_marcas = {una_marca['id']: una_marca for una_marca in marcas}

            #Obtener todos los proveedores y armar un index {id, dict}
            proveedores = transaccion.obtenerReg("SELECT * FROM PROVEEDORES")
            index_prov = {un_proveedor['id']: un_proveedor for un_proveedor in proveedores}
            
            #Obtener todas las categorias y armar un index {id, dict}
            categorias = transaccion.obtenerReg("SELECT * FROM CATEGORIAS")
            index_cats = {una_categ['id']: una_categ for una_categ in categorias}

            #Obtener la relacion entre articulos y categorias, y armar un index {id, lstas(ids cat)}
            arts_cats = transaccion.obtenerReg("SELECT * FROM ARTICULOS_CATEGORIAS")
            index_art_cat = {}
            for un_art_cat in arts_cats:
                if un_art_cat['articulo_id'] not in index_art_cat:
                    #si no existe el articulo en el indice se agrega con una lista de ids vacia
                    index_art_cat[un_art_cat['articulo_id']] = []
                #agregar categoria
                index_art_cat[un_art_cat['articulo_id']].append(un_art_cat['categoria_id'])

            #Obtener todos los articulos y generar la respuesta final
            articulos = transaccion.obtenerReg("SELECT * FROM ARTICULOS")
            
            lista_articulos = []
            for un_articulo in articulos:
                
                articulo_final = un_articulo.copy()

                #Reemplazar el id de la marca por su dict
                marca_id = articulo_final.pop('marca_id', None) 
                articulo_final['marca'] = index_marcas.get(marca_id) 
                
                #Reemplazar el id del proveedor por su dict
                proveedor_id = articulo_final.pop('proveedor_id', None) 
                articulo_final['proveedor'] = index_prov.get(proveedor_id) 
                
                #Agregar las categorias
                sus_categorias = []
                #Obtener los IDs de categorías
                sus_ids_categorias = index_art_cat.get(articulo_final['id'], [])
                #Obtener los datos de las categorias y agregarlos
                for categ_id in sus_ids_categorias:
                    sus_categorias.append(index_cats[categ_id])
                articulo_final['categorias'] = sus_categorias

                #Añadir este articulo al resultado
                lista_articulos.append(articulo_final)
            #Finalizar
            transaccion.confirmar_transaccion()
            return lista_articulos
        except Exception as err:
            print(f"Error al obtener los artículos: {err}")
            return {}
        finally:
            if transaccion:
                transaccion.finalizar_transaccion()

    #----Metodo estatico para obtener un articulo
    @staticmethod
    def get_one(id: int) -> dict:
        transaccion = None
        try:
            transaccion = TransaccionBD()
            transaccion.iniciar_transaccion()
            
            #Obtener el articulo
            articulos = transaccion.obtenerReg("SELECT * FROM ARTICULOS WHERE id=%s",(id,))
            if articulos == {}:
                return {}
            articulo_final = articulos[0]
        
            #Obtener la marca del articulo
            marca = transaccion.obtenerReg("SELECT * FROM MARCAS WHERE id=%s",(articulo_final['marca_id'],))[0]
   
            #Obtener el proveedores del articulo
            proveedor = transaccion.obtenerReg("SELECT * FROM PROVEEDORES WHERE id=%s",(articulo_final['proveedor_id'],))[0]
           
            #Obtener todas las categorias
            art_cat = transaccion.obtenerReg( "SELECT ARTICULOS_CATEGORIAS.categoria_id " \
                                             "FROM ARTICULOS_CATEGORIAS " \
                                             "WHERE ARTICULOS_CATEGORIAS.articulo_id = %s", (id,))
            #Armado del resutalado
            categorias = []
            for una_cat in art_cat:
                #Obtener la categoria
                una_categ = transaccion.obtenerReg("SELECT * FROM CATEGORIAS WHERE id=%s",(una_cat['categoria_id'],))
                categorias.append(una_categ[0])

            #Reemplazar el id de la marca por su dict
            articulo_final.pop('marca_id')
            articulo_final['marca'] = marca

            #Reemplazar el id del proveedor por su dict
            articulo_final.pop('proveedor_id') 
            articulo_final['proveedor'] = proveedor

            #Agregar las categorias
            articulo_final['categorias'] = categorias
            transaccion.confirmar_transaccion()
            return articulo_final
        except Exception as err:
            print(f"Error al obtener artículo {id}: {err}")
            return {}
        finally:
            if transaccion:
                transaccion.finalizar_transaccion()

    #----Metodo para crear un articulo
    def create(self, data: dict) -> bool | None:

        transaccion = None
        try:
            transaccion = TransaccionBD()
            transaccion.iniciar_transaccion()

            #Obtener los dict/list internos
            marca = data['marca']
            proveedor = data['proveedor']
            categorias = data['categorias']

            #Insertar el articulo
            if not transaccion.operacionBD("INSERT INTO ARTICULOS (descripcion, precio, stock, marca_id, proveedor_id) VALUES  (%s, %s, %s, %s, %s)",
                                                (data['descripcion'],data['precio'],data['stock'],marca['id'],proveedor['id'],)):
                transaccion.revertir_transaccion()
                return False
            id_art = transaccion.get_nuevo_id()

            #Insertar la relacion Articulos-Categorias
            for una_cat in categorias:   
                if not transaccion.operacionBD("INSERT INTO ARTICULOS_CATEGORIAS (articulo_id,categoria_id) VALUES (%s, %s)",
                                                (id_art, una_cat['id'],)):
                    transaccion.revertir_transaccion()
                    return False
                
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

            #Obtener los dict/list internos
            marca = data['marca']
            proveedor = data['proveedor']
            categorias = data['categorias']

            #Actualizar el articulo
            if not transaccion.operacionBD("UPDATE ARTICULOS SET descripcion=%s, precio=%s, stock=%s, marca_id=%s, proveedor_id=%s " \
                                        "WHERE id=%s",(data['descripcion'],data['precio'],data['stock'],marca['id'],proveedor['id'],data['id'])):
                transaccion.revertir_transaccion()
                return False
            
            #Eliminar las categorias anteriores
            if not transaccion.operacionBD("DELETE FROM ARTICULOS_CATEGORIAS WHERE articulo_id=%s",(data['id'],)):
                transaccion.revertir_transaccion()
                return False 
            
            #Agregar las categorias nuevas
            for una_cat in categorias:
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
