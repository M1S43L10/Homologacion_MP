from conexiones import *
import sys
sys.path.append(r"C:\Users\Op_1111\Desktop\Codigos_GitHub\Homologacion_MP")
from Class_MP.Conexion_APIs_MP import Conexion_Api
from Class_MP.database import ConexionSybase
import time
from datetime import datetime, timedelta


# Obtener la fecha y hora actual
now = datetime.now()

# Calcular la fecha y hora hace 24 horas
twenty_four_hours_ago = now - timedelta(hours=24)

# Formatear las fechas
formato_fecha = now.strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]  # Se omiten los últimos 3 caracteres para tener solo los milisegundos

#-----------------------------------------------------------------------------------------------------------------
#CONEXION A BASE DE DATOS
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


#CONEXION A INTERFAZ MPQRCODE
"""if __name__ == "__main__":
    app = InterfazMercadoPago()
    app.mainloop()"""

#CONEXION A MODULO API
app = Conexion_Api("1613246141", "APP_USR-3422573537375961-122909-c6e6f9acb178c3efffcd667996c26b15-1613246141")
instanciacion = Conexion_APP(app, conexion_sybase)




"""
instanciacion.limpieza_tabla_sucursal()
instanciacion.limpieza_tabla_caja()
"""
"""
instanciacion.limpieza_tabla_TOTALsucursal()
instanciacion.limpieza_tabla_TOTALcaja()
"""
#instanciacion.creacionSUC("SUC002")
#instanciacion.crearCaja("SUC002")


"""
conexion_sybase.eliminar_tabla("MPQRCODE_CREARORDEN")
conexion_sybase.crear_tabla_MPQRCODE_CREARORDEN()

conexion_sybase.crear_tabla_MPQRCODE_CREARORDEN_items()
"""

#conexion_sybase.eliminar_filas("MPQRCODE_SUCURSAL", "id", 59270546)

#instanciacion.eliminarSUC("SUC002")
#instanciacion.eliminarCaja("SUC001POS003")



nro_factura = input("Ingrese el NRO de FACTURA: ")

precio = 1000
external_idPOS = "SUC002POS001"

tabla = 'MPQRCODE_CREARORDEN'
columna = 'date_creation'

crear_ORDEN = app.crear_orden(precio, external_idPOS, nro_factura)
if crear_ORDEN.status_code >= 200 and crear_ORDEN.status_code < 300:
    id_increment = conexion_sybase.inicializar_tablas_OBTIENEIDINCREMET(tabla, columna, formato_fecha)
    conexion_sybase.insertar_dato_en_tabla(tabla, 'external_reference', id_increment, external_idPOS)
    try:
        datos = []
        for clave_json, valor_json in crear_ORDEN.json():
            if isinstance(valor_json, list):
                if clave_json == 'items':
                    for recorre_lista in valor_json:
                        print(len(recorre_lista))
    except:
        print("ERROR")
        #conexion_sybase.eliminar_tabla(tabla)
        #conexion_sybase.crear_tabla_MPQRCODE_CREARORDEN()
                    
    
    """
    obtener_ID = None
    while obtener_ID is None:
        print(id_value)
        obtener_ID = conexion_sybase.obtener_id_compra(crear_ORDEN[1], crear_ORDEN[2])
        
        if obtener_ID is None:
            print("Esperando a que se actualice el ID en la base de datos...")
            time.sleep(5)  # Puedes ajustar el tiempo de espera según sea necesario
    conexion_sybase.actualizar_id_pago_MERCHANTORDEN(crear_ORDEN[1], crear_ORDEN[2], obtener_ID[1], obtener_ID[2])
    print("Pago Realizado. ID obtenido:", obtener_ID[2])"""

#respuesta1 = app.crear_ordenV2("SUC002", "SUC002POS001")

#respuesta1 = app.obtener_ordenV2("SUC002POS001")
#print(respuesta1)

#Crear Orden DINAMICO
#app.crear_orden_dinamico(1800, "Anonimo", "Ca_0101")

