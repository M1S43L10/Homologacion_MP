import pypyodbc
import json
import time


class ConexionSybase:
    def __init__(self, **kwargs):
        self.conexion = None
        self.cursor = None
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
            self.cursor = self.conexion.cursor()  # Crea el cursor
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
    def crear_tabla(self, nombre_tabla):
        try:
            self.conectar()
            query = f"""
                CREATE TABLE {nombre_tabla} (
                    ID INT IDENTITY,
                    FECHA_CREACION DATETIME,
                    NRO_FACTURA VARCHAR(255) PRIMARY KEY,
                    PUNTO_VENTA VARCHAR(255),
                    ID_PAGO VARCHAR(255),
                )
            """
            self.cursor.execute(query)
            self.conexion.commit()
            print(f'Tabla {nombre_tabla} creada con éxito.')
        except Exception as e:
            print(f'Error al crear la tabla: {e}')
        finally:
            self.desconectar()



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
            
    def verificar_existencia_tabla(self, nombre_tabla):
        try:
            with self.conexion.cursor() as cursor:
                consulta = f"SELECT COUNT(*) FROM SYSTABLE WHERE TABLE_NAME = '{nombre_tabla}'"
                cursor.execute(consulta)
                cantidad = cursor.fetchone()[0]
                return cantidad > 0
        except pypyodbc.Error as err:
            print(f"Error al verificar la existencia de la tabla: {err}")
            return False


    def eliminar_tabla(self, nombre_tabla):
        try:
            if self.conectar():  # Llama a conectar antes de continuar
                if self.verificar_existencia_tabla(nombre_tabla):
                    with self.conexion.cursor() as cursor:
                        consulta = f"DROP TABLE {nombre_tabla}"
                        cursor.execute(consulta)
                        print(f"Tabla '{nombre_tabla}' eliminada exitosamente.")
                else:
                    print(f"La tabla '{nombre_tabla}' no existe en la base de datos.")
            else:
                print("Error al conectar a la base de datos.")
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

    # MANEJO DE DATOS DE UNA TABLA
    def insertar_datos(self, tabla, datos):
        try:
            self.conectar()
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
        finally:
            self.desconectar()

    def insertar_datos_MERCHANT(self, NRO_FACTURA, PUNTO_VENTA):
        datos = {
            'NRO_FACTURA': NRO_FACTURA,
            'PUNTO_VENTA': PUNTO_VENTA
        }
        self.insertar_datos('MERCHANTORDEN', datos)

            
    def actualizar_id_pago(self, factura, POS, ID_PAGO):
        try:
            self.conectar()

            # Verificar si existe una fila con la combinación de NRO_FACTURA y PUNTO_VENTA
            if self.existe_fila(factura, POS):
                with self.conexion.cursor() as cursor:
                    # Ejecutar la consulta para actualizar el ID_PAGO
                    query = f"UPDATE MERCHANTORDEN SET ID_PAGO = '{ID_PAGO[0]}' WHERE NRO_FACTURA = '{factura}' AND PUNTO_VENTA = '{POS}'"
                    cursor.execute(query)
                    self.conexion.commit()

                    print(f"ID_PAGO actualizado exitosamente para la factura {POS}.")
            else:
                print(f"No se encontró una fila con NRO_FACTURA='{factura}' y PUNTO_VENTA='{POS}' en la base de datos.")
        except pypyodbc.Error as err:
            print(f"Error al actualizar ID_PAGO: {err}")
        finally:
            self.desconectar()


    def existe_fila(self, numero_factura, punto_venta):
        try:
            with self.conexion.cursor() as cursor:
                # Ejecutar la consulta para verificar la existencia de la fila
                query = f"SELECT 1 FROM MERCHANTORDEN WHERE NRO_FACTURA = '{numero_factura}' AND PUNTO_VENTA = '{punto_venta}'"
                cursor.execute(query)

                # Obtener el resultado de la consulta
                resultado = cursor.fetchone()

                # Si se encontró un resultado, la fila existe
                return resultado is not None
        except pypyodbc.Error as err:
            print(f"Error al verificar la existencia de la fila: {err}")
            return False

    
    # MANEJO DE DATOS DE UNA TABLA
    def obtener_id_compra(self, numero_factura, punto_venta):
        try:
            with self.conexion.cursor() as cursor:
                # Ejecutar la consulta para obtener el ID de compra y ID_PAGO
                query = f"SELECT ID_PAGO FROM MERCHANTORDEN WHERE NRO_FACTURA = '{numero_factura}' AND PUNTO_VENTA = '{punto_venta}'"
                cursor.execute(query)

                # Obtener el resultado de la consulta
                resultado = cursor.fetchone()

                if resultado is not None:
                    # Si se encontró un resultado, devolver el ID de compra y ID_PAGO
                    id_pago = resultado
                    print(f"ID_PAGO para factura {numero_factura} y POS {punto_venta}: {id_pago}")
                    return id_pago
                else:
                    # Si no se encontró ninguna coincidencia, devolver None
                    print(f"No se encontró una fila con NRO_FACTURA='{numero_factura}' y PUNTO_VENTA='{punto_venta}'.")
                    return None
        except pypyodbc.Error as err:
            print(f"Error al obtener el ID de compra: {err}")
            return None


    #DESCONEXION DE LA BASE DE DATOS
    def desconectar(self):
        if self.conexion and self.conexion.connected:
            self.conexion.close()
            print("Conexión a Sybase cerrada.")
        else:
            print("La conexión ya estaba cerrada.")

            



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
        
        conexion_sybase.obtener_id_compra("Factura-0001")


        conexion_sybase.desconectar()
    else:
        print("Error al conectar a Sybase.")