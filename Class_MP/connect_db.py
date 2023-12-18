import pypyodbc

class ConexionSybase:
    def __init__(self, **kwargs):
        self.conector = pypyodbc.connect(**kwargs)
        self.usuario = kwargs["user"]
        self.contrasena = kwargs["password"]
        self.base_datos = kwargs["database"]
        self.conexion_cerrada = False
        self.conexion = None

    def conectar(self):
        try:
            self.conexion = pypyodbc.connect(
                user=self.usuario,
                password=self.contrasena,
                database=self.base_datos,
                Driver="{Adaptive Server Anywhere 9.0}",
                ServerName="gestionih1111",  # Reemplaza con tu servidor Sybase
                Port="2638",  # Reemplaza con el puerto Sybase
                PWD=self.contrasena,
                FILE=self.base_datos,  # Ruta completa al archivo de base de datos
            )
            return True
        except pypyodbc.Error as err:
            print(f"Error al conectar a Sybase: {err}")
            return False

    def mostrar_tablas(self):
        try:
            with self.conexion.cursor() as cursor:
                consulta = """
                    SELECT table_name
                    FROM INFORMATION_SCHEMA.TABLES
                    WHERE table_type = 'BASE TABLE'
                """
                cursor.execute(consulta)
                filas = cursor.fetchall()

                print("Lista de tablas en la base de datos:")
                for fila in filas:
                    print(fila[0])
        except pypyodbc.Error as err:
            print(f"Error al mostrar las tablas: {err}")

    def desconectar(self):
        if self.conexion:
            self.conexion.close()
            print("Conexión a Sybase cerrada.")

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

    def eliminar_base_de_datos(self, nombre_bd):
        try:
            with self.conexion.cursor() as cursor:
                consulta = f"DROP DATABASE {nombre_bd}"
                cursor.execute(consulta)
                print(f"Base de datos '{nombre_bd}' eliminada exitosamente.")
        except pypyodbc.Error as err:
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
        except pypyodbc.Error as err:
            print(f"Error al seleccionar la tabla '{nombre_tabla}': {err}")

# Ejemplo de uso
if __name__ == "__main__":
    # Reemplaza los valores con la información correcta para tu conexión Sybase
    configuracion_sybase = {
        "user": "dba",
        "password": "gestion",
        "database": "I:\Misa\tentollini_DBA 2023-12-11 12;05;28\Dba\gestionh.db",
        # Agrega otros parámetros según sea necesario
    }

    conexion_sybase = ConexionSybase(**configuracion_sybase)

    if conexion_sybase.conectar():
        print("Conexión exitosa a Sybase.")

        # Realiza las operaciones que necesites con la conexión Sybase
        conexion_sybase.mostrar_tablas() 
        conexion_sybase.desconectar()
    else:
        print("Error al conectar a Sybase.")
