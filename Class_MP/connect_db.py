import pypyodbc
import json
import os

class ConexionSybase:
    def __init__(self, **kwargs):
        self.conexion = None
        self.usuario = kwargs["user"]
        self.contrasena = kwargs["password"]
        self.base_datos = kwargs["database"]

    #CONEXION DE LA BASE DE DATOS
    def conectar(self):
        try:
            self.conexion = pypyodbc.connect(
                user=self.usuario,
                password=self.contrasena,
                database=self.base_datos,
                Driver="{Adaptive Server Anywhere 9.0}",
                DSN="GestionIH1111",  # Nombre del DSN configurado en tu sistema
                PWD=self.contrasena,
                FILE=self.base_datos,  # Ruta completa al archivo de base de datos
            )
            return True
        except pypyodbc.Error as err:
            print(f"Error al conectar a Sybase: {err}")
            return False
        
        
    #MANEJO A LA BASE DE DATOS
    def eliminar_base_de_datos(self, nombre_bd):
        try:
            with self.conexion.cursor() as cursor:
                consulta = f"DROP DATABASE {nombre_bd}"
                cursor.execute(consulta)
                print(f"Base de datos '{nombre_bd}' eliminada exitosamente.")
        except pypyodbc.Error as err:
            print(f"Error al eliminar la base de datos: {err}")
            
        
    #MANEJOS DE TABLAS
    
    def crear_tabla(self, tabla, columnas):
        try:
            with self.conexion.cursor() as cursor:
                consulta = f"CREATE TABLE {tabla} ({columnas})"
                cursor.execute(consulta)
                print(f"Tabla '{tabla}' creada exitosamente.")
        except pypyodbc.Error as err:
            print(f"Error al crear la tabla: {err}")
    
    def mostrar_tablas(self, nombre_bda):
        try:
            with self.conexion.cursor() as cursor:
                consulta = f"""
                    SELECT table_name
                    FROM {nombre_bda}..SYSTABLE
                """
                cursor.execute(consulta)
                filas = cursor.fetchall()

                print("Lista de tablas en la base de datos:")
                for fila in filas:
                    print(fila[0])
        except pypyodbc.Error as err:
            print(f"Error al mostrar las tablas: {err}")
    
    def actualizar_tabla(self, nombre_tabla, columnas_actualizadas):
        try:
            with self.conexion.cursor() as cursor:
                consulta = f"ALTER TABLE {nombre_tabla} {columnas_actualizadas}"
                cursor.execute(consulta)
                print(f"Tabla '{nombre_tabla}' actualizada exitosamente.")
        except pypyodbc.Error as err:
            print(f"Error al actualizar la tabla: {err}")

    def eliminar_tabla(self, nombre_tabla):
        try:
            with self.conexion.cursor() as cursor:
                consulta = f"DROP TABLE {nombre_tabla}"
                cursor.execute(consulta)
                print(f"Tabla '{nombre_tabla}' eliminada exitosamente.")
        except pypyodbc.Error as err:
            print(f"Error al eliminar la tabla: {err}")
            
    def limpiar_tabla(self, tabla):
        try:
            with self.conexion.cursor() as cursor:
                consulta = f"DELETE FROM {tabla}"
                cursor.execute(consulta)
                self.conexion.commit()
                print(f"Tabla '{tabla}' limpiada exitosamente.")
        except pypyodbc.Error as err:
            print(f"Error al limpiar la tabla: {err}")

    def seleccionar_tabla(self, nombre_tabla):
        try:
            with self.conexion.cursor() as cursor:
                consulta = f"SELECT * FROM {nombre_tabla}"
                cursor.execute(consulta)
                filas = cursor.fetchall()

                print(f"Contenido de la tabla '{nombre_tabla}':")
                for fila in filas:
                    print(fila)
        except pypyodbc.Error as err:
            print(f"Error al seleccionar la tabla '{nombre_tabla}': {err}")            

    #MANEJO DE DATOS DE UNA TABLA
    def insertar_datos(self, tabla, datos):
        try:
            with self.conexion.cursor() as cursor:
                # Construir la consulta SQL de inserción
                columnas = ", ".join([f'"{col}"' for col in datos.keys()])
                valores = ", ".join([f"'{v}'" if not isinstance(v, dict) else f"'{json.dumps(v)}'" for v in datos.values()])
                consulta = f'INSERT INTO {tabla} ({columnas}) VALUES ({valores})'
                cursor.execute(consulta)
                self.conexion.commit()
                print(f"Datos insertados en la tabla '{tabla}' exitosamente.")
        except pypyodbc.Error as err:
            print(f"Error al insertar datos: {err}")
            
    #DESCONEXION DE LA BASE DE DATOS
    def desconectar(self):
        if self.conexion:
            self.conexion.close()
            print("Conexión a Sybase cerrada.")
            



# Ejemplo de uso
if __name__ == "__main__":
    # Reemplaza los valores con la información correcta para tu conexión Sybase
    configuracion_sybase = {
        "user": "dba",
        "password": "gestion",
        "database": r"I:\Misa\tentollini_DBA 2023-12-11 12;05;28\Dba\gestionh.db",
        # Agrega otros parámetros según sea necesario
    }

    conexion_sybase = ConexionSybase(**configuracion_sybase)

    if conexion_sybase.conectar():
        print("Conexión exitosa a Sybase.")

        # Ruta completa del archivo JSON
        ruta_json = os.path.join("Anonimo_CAJAS_JSON", "Ca_0101.json")

        try:
            # Cargar datos desde el archivo JSON
            with open(ruta_json, "r", encoding="utf-8") as archivo_json:
                datos_json = json.load(archivo_json)

            # Insertar datos en la tabla correspondiente
            conexion_sybase.insertar_datos("MP_CAJAS ", datos_json)
        except FileNotFoundError:
            print(f"Archivo JSON no encontrado: {ruta_json}")
        except json.JSONDecodeError as json_err:
            print(f"Error al decodificar el JSON: {json_err}")

        conexion_sybase.desconectar()
    else:
        print("Error al conectar a Sybase.")