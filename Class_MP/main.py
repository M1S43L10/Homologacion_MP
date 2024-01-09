from conexiones import *
import sys
sys.path.append(r"C:\Users\Op_1111\Desktop\Codigos_GitHub\Homologacion_MP")
from Class_MP.Conexion_APIs_MP import Conexion_Api
from Class_MP.database import ConexionSybase
import time

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
app = ("1627358269", "APP_USR-8914848154505078-010809-0a345be95bb83eb5f90fa62663f7cad8-1627358269")
instanciacion = Conexion_APP(app, conexion_sybase)
"""
instanciacion.limpieza_tabla_TOTALsucursal()
instanciacion.limpieza_tabla_TOTALcaja()
instanciacion.eliminarOrdenesPostDBA()
"""

"""
/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*LIMPIEZA/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*

instanciacion.limpieza_tabla_sucursal()
instanciacion.limpieza_tabla_caja()


"""

"""
/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*SUCURSAL/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*
"""
#instanciacion.eliminarSUC("SUC002")
"""
datosSUC = {
    'business_hours': {
        'monday': [{'open': '08:00', 'close': '12:00'}], 
        'tuesday': [{'open': '08:00', 'close': '12:00'}], 
        'wednesday': [{'open': '08:00', 'close': '12:00'}], 
        'thursday': [{'open': '08:00', 'close': '12:00'}], 
        'friday': [{'open': '08:00', 'close': '12:00'}], 
        'saturday': [{'open': '08:00', 'close': '12:00'}], 
        'sunday': [{'open': '08:00', 'close': '12:00'}]}, 
    'external_id': 'SUC001', 
    'location': {
        'street_number': '197', 
        'street_name': 'Santa Fe', 
        'city_name': 'Resistencia', 
        'state_name': 'Chaco', 
        'latitude': -27.44817655900252, 
        'longitude': -58.986462728116216, 
        'reference': 'Esquina'}, 
    'name': ' Inforhard'}

instanciacion.creacionSUC(datosSUC)
"""
"""
/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*CAJAS/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*

#instanciacion.eliminarCaja("SUC001POS003")
"""
#instanciacion.crearCaja("SUC001")

#/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*CREAR ORDEN/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*
"""pago = instanciacion.crearOrden("SUC001POS001")
id_pago = instanciacion.obteneridOrder(pago[0], pago[1])
instanciacion.obtenerPago(id_pago, pago[0], pago[1])

"""
"""
conexion_sybase.eliminar_tabla("MPQRCODE_CLIENTE")
conexion_sybase.crear_tabla_MPQRCODE_CLIENTE()"""


#conexion_sybase.eliminar_filas("MPQRCODE_SUCURSAL", "id", 59270546)


#respuesta1 = app.crear_ordenV2("SUC002", "SUC002POS001")

#respuesta1 = app.obtener_ordenV2("SUC002POS001")
#print(respuesta1)

#Crear Orden DINAMICO
#app.crear_orden_dinamico(1800, "Anonimo", "Ca_0101")

