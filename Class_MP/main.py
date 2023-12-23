import sys
sys.path.append(r"C:\Users\Op_1111\Desktop\Codigos_GitHub\Homologacion_MP")
from Class_MP.Conexion_APIs_MP import Conexion_Api
from Class_MP.connect_db import ConexionSybase
from datetime import datetime, timedelta

# Obtener la fecha y hora actual
now = datetime.now()

# Calcular la fecha y hora hace 24 horas
twenty_four_hours_ago = now - timedelta(hours=24)

# Formatear las fechas
formatted_now = now.strftime('%Y-%m-%d %H:%M:%S')
formatted_twenty_four_hours_ago = twenty_four_hours_ago.strftime('%Y-%m-%d %H:%M:%S')

#Ejemplo de uso
if __name__ == "__main__":
    # Reemplaza los valores con la información correcta para tu conexión Sybase
    configuracion_sybase = {
        "user": "dba",
        "password": "gestion",
        "database": r"I:\Misa\tentollini_DBA 2023-12-11 12;05;28\Dba\gestionh.db",
        # Agrega otros parámetros según sea necesario
    }

    conexion_sybase = ConexionSybase(**configuracion_sybase)

"""if __name__ == "__main__":
    app = InterfazMercadoPago()
    app.mainloop()"""


app = Conexion_Api("1588285685", "APP_USR-3774512295656164-121208-e45df91faddd6fd608de107d1db2971f-1588285685")

#Crear Sucursal
#app.crear_sucursal("08:00", "13:00", "SUC002")

#Crear Caja
#app.crear_caja("Anonimo")

#Crear Orden ATENDIDO
#app.crear_orden(1000, "SUC002POS001")

conexion_sybase.crear_tabla("MERCHANTORDEN")

"""nro_factura = input("Ingrese el NRO de FACTURA: ")

crear_ORDEN = app.crear_orden(1000, "SUC002POS001", nro_factura)

def orden_creada():
    return crear_ORDEN[1], crear_ORDEN[2]

if crear_ORDEN[0] >= 200 and crear_ORDEN[0] < 300:
    conexion_sybase.insertar_datos_MERCHANT(crear_ORDEN[1], crear_ORDEN[2])    
    obtener_ID = None    
    while obtener_ID is None:
        obtener_ID = conexion_sybase.obtener_id_compra(crear_ORDEN[1], crear_ORDEN[2])
    print(f"PagoRealizado. ID obtenido: {obtener_ID}")"""
#respuesta1 = app.crear_ordenV2("SUC002", "SUC002POS001")

#respuesta1 = app.obtener_ordenV2("SUC002POS001")
#print(respuesta1)

#Crear Orden DINAMICO
#app.crear_orden_dinamico(1800, "Anonimo", "Ca_0101")