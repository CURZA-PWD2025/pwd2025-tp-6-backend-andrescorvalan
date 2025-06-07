import mysql.connector
import os
from dotenv import load_dotenv

load_dotenv()

#Clase para realizar operaciones sobre la BD que sean unicas (select, insert, update, delete), con autocommin=True
class OperarBD:

    #----Metodo estatico para obtener una conexion a la bd
    @staticmethod
    def get_connect():
        try:
            conn = mysql.connector.connect(
                user = os.getenv('DB_USER'),
                password = os.getenv('DB_PASSWORD'),
                database = os.getenv('DB_NAME'),
                host = os.getenv('DB_HOST'),
                port = os.getenv('DB_PORT'),
                autocommit = True,              #cada operacion (insert, update, delete) sera tratada como una transaccion (se commitea solo)
            )
            return conn
        except mysql.connector.Error as una_excepccion:
            print(f'Ocurrio una excepcion al intentar conectarse a la base de datos: {una_excepccion}')
            raise

    #---Metodo estatico para obtener resgistros, se debe usar con SELECT en el parametro sql
    # Retorna: - Un conjunto de registros.
    #          - [] si el conjunto es vacio o hubo algun error de la BD
    @staticmethod
    def obtenerReg(sql: str, params: tuple=()) -> list[dict]:
        conexion = None
        try:
            conexion = OperarBD.get_connect()
            with conexion.cursor(dictionary=True) as un_cursor:
                un_cursor.execute(sql,params)
                return un_cursor.fetchall()
        except mysql.connector.Error as una_excepccion:
            print(f'Error al intentar obtener datos de la BD {una_excepccion}')
            return []
        finally:
            if conexion and conexion.is_connected():
                conexion.close()

    #---Metodo estatico para modificar resgistros, se debe usar con INSERT, UPDATE o DELETE en el parametro sql
    # Retorna: - False si la operacion no fue exitosa
    #          - True si la operacion fue exitosa
    #          - Un entero si una operacion de insert fue exitosa y se genero automaticamente un Id (PK autoincrement)
    #          - None si se detecto una excepcion
    @staticmethod
    def modifBD(sql: str, params: tuple=()) -> int | bool | None:
        conexion = None
        try:
            conexion = OperarBD.get_connect()
            with conexion.cursor(dictionary=True) as un_cursor:
                un_cursor.execute(sql, params)
                if un_cursor.rowcount == 1:
                    if sql.strip().upper().startswith("INSERT") and un_cursor.lastrowid:
                        return un_cursor.lastrowid              # Devuelve el ID generado para INSERT
                    else:
                        return True
                else:
                    return False
        except mysql.connector.Error as una_excepccion:
            print(f'Error de conexion a la B o al intentar insertar datos: {una_excepccion}')
            return None
        finally:
            if conexion and conexion.is_connected():
                conexion.close()

#Clase para realizar operaciones sobre la BD que NO sean unicas, sino varias en una transaccion (autocommit=False)
class TransaccionBD:
    def __init__(self):
        self.conexion = None
        self.cursor = None
        self.nuevo_id = 0 # Almacena el último ID generado (si se inserto en una tabla con PK autoincrement)


    def get_nuevo_id(self):
        return self.nuevo_id
    
    #----Metodo para inicializar una transaccion y su conexion
    def iniciar_transaccion(self):
        if self.conexion and self.conexion.is_connected():  #por si quedo una transaccion activa
            self.finalizar_transaccion() 
        try:
            self.conexion = mysql.connector.connect(
                user = os.getenv('DB_USER'),
                password = os.getenv('DB_PASSWORD'),
                database = os.getenv('DB_NAME'),
                host = os.getenv('DB_HOST'),
                port = os.getenv('DB_PORT'),
                autocommit = False
            )
            self.cursor = self.conexion.cursor(dictionary=True)
            self.nuevo_id = 0
        except mysql.connector.Error as una_excepccion:
            raise RuntimeError(f'Ocurrio una excepcion al intentar iniciar la transaccion: {una_excepccion}') 

    #----Metodo para hacer un commit
    def confirmar_transaccion(self):
        if self.conexion and self.conexion.is_connected():
            self.conexion.commit()
        else:
            raise RuntimeError("No hay una transaccion activa para realizer un commit.")

   #----Metodo para hacer un rollback
    def revertir_transaccion(self):
        if self.conexion and self.conexion.is_connected():
            self.conexion.rollback()
        else:
            raise RuntimeError("No hay una transaccion activa para realizer un rollback.")

    #----Metodo para finalizar la transaccion, liberando los recursos
    def finalizar_transaccion(self):
        if self.cursor:
            try:
                self.cursor.close()
            except mysql.connector.Error as err:
                print(f"Error al cerrar el cursor: {err}")
            finally:
                self.cursor = None
        if self.conexion and self.conexion.is_connected():
            try:
                self.conexion.close() 
            except mysql.connector.Error as err:
                print(f"Error al cerrar la conexion: {err}")
            finally: 
                self.conexion = None
    
    #----Metodo para obtener datos de la BD (SELECT)
    def obtenerReg(self, sql: str, params: tuple=()) -> list[dict]:
        if not self.conexion or not self.conexion.is_connected():
            raise RuntimeError("obtenerReg(): no se esta dentro de una una transaccion")
        self.cursor.execute(sql, params)
        return self.cursor.fetchall()
    
    #----Metodo para modificar datos de la BD (INSERT,UPDATE,DELETE)
    # Retorna: - False si la operacion no fue exitosa
    #          - True si la operacion fue exitosa
    def operacionBD(self, sql: str, params: tuple=()) -> bool:
        if not self.conexion or not self.conexion.is_connected():
            raise RuntimeError("Operacion de DML: no se está dentro de una transacción activa.")
       
        self.cursor.execute(sql, params)
        if self.cursor.rowcount >= 1:
            self.nuevo_id = self.cursor.lastrowid #Guardar el nuevo ID
            return True
        else:
            return False