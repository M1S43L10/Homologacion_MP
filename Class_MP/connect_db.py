import pymysql

class ConexionMySQL:
    def __init__(self, **kwargs):
        self.conector = pymysql.connect(**kwargs)
        self.host = kwargs["host"]
        self.usuario = kwargs["user"]
        self.contrasena = kwargs["password"]
        self.base_datos = kwargs["database"]
        self.conexion_cerrada = False
        self.conexion = None

    def conectar(self):
        try:
            self.conexion = pymysql.connect(
                host=self.host,
                user=self.usuario,
                password=self.contrasena,
                database=self.base_datos
            )
            return True
        except pymysql.Error as err:
            print(f"Error al conectar a MySQL: {err}")
            return False

    def desconectar(self):
        if self.conexion:
            self.conexion.close()
            print("Conexión a MySQL cerrada.")

    def crear_base_de_datos(self, nombre_nueva_bd):
        try:
            with self.conexion.cursor() as cursor:
                cursor.execute(f"CREATE DATABASE {nombre_nueva_bd}")
                print(f"Base de datos '{nombre_nueva_bd}' creada exitosamente.")
        except pymysql.Error as err:
            print(f"Error al crear la base de datos: {err}")

    def crear_tabla(self, nombre_tabla, columnas):
        try:
            with self.conexion.cursor() as cursor:
                consulta = f"CREATE TABLE {nombre_tabla} ({columnas})"
                cursor.execute(consulta)
                print(f"Tabla '{nombre_tabla}' creada exitosamente.")
        except pymysql.Error as err:
            print(f"Error al crear la tabla: {err}")

    def actualizar_tabla(self, nombre_tabla, columnas_actualizadas):
        try:
            with self.conexion.cursor() as cursor:
                consulta = f"ALTER TABLE {nombre_tabla} {columnas_actualizadas}"
                cursor.execute(consulta)
                print(f"Tabla '{nombre_tabla}' actualizada exitosamente.")
        except pymysql.Error as err:
            print(f"Error al actualizar la tabla: {err}")

    def eliminar_tabla(self, nombre_tabla):
        try:
            with self.conexion.cursor() as cursor:
                consulta = f"DROP TABLE {nombre_tabla}"
                cursor.execute(consulta)
                print(f"Tabla '{nombre_tabla}' eliminada exitosamente.")
        except pymysql.Error as err:
            print(f"Error al eliminar la tabla: {err}")

    def eliminar_base_de_datos(self, nombre_bd):
        try:
            with self.conexion.cursor() as cursor:
                consulta = f"DROP DATABASE {nombre_bd}"
                cursor.execute(consulta)
                print(f"Base de datos '{nombre_bd}' eliminada exitosamente.")
        except pymysql.Error as err:
            print(f"Error al eliminar la base de datos: {err}")

    def seleccionar_tabla(self, nombre_tabla):
        try:
            with self.conexion.cursor() as cursor:
                consulta = f"SELECT * FROM {nombre_tabla}"
                cursor.execute(consulta)
                filas = cursor.fetchall()
                
                print(f"Contenido de la tabla '{nombre_tabla}':")
                for fila in filas:
                    print(fila)
        except pymysql.Error as err:
            print(f"Error al seleccionar la tabla '{nombre_tabla}': {err}")




"""# Ejemplo de uso
if __name__ == "__main__":
    conexion_mysql = ConexionMySQL()
    conexion_mysql.conectar()

    # Crear una nueva base de datos
    conexion_mysql.crear_base_de_datos("MercadoPagoQR")

    # Desconectar para luego conectar a la nueva base de datos
    conexion_mysql.desconectar()

    # Conectar a la nueva base de datos
    conexion_mysql.base_datos = "MercadoPagoQR"
    conexion_mysql.conectar()

    # Crear una tabla de ejemplo
    columnas_ejemplo = "id INT PRIMARY KEY, nombre VARCHAR(255), edad INT"
    conexion_mysql.crear_tabla("Sucursal", columnas_ejemplo)

    # Actualizar la tabla de ejemplo
    columnas_actualizadas = "ADD COLUMN direccion VARCHAR(255)"
    conexion_mysql.actualizar_tabla("Sucursal", columnas_actualizadas)

    # Eliminar la tabla de ejemplo
    #conexion_mysql.eliminar_tabla("Sucursal")

    # Eliminar la base de datos creada
    #conexion_mysql.eliminar_base_de_datos("MercadoPagoQR")

    conexion_mysql.desconectar()
"""