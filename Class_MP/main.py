import os
import sys
directorio_script = os.path.dirname(os.path.abspath(__file__))
# Construir la ruta relativa al directorio que deseas agregar
ruta_relativa = os.path.join(directorio_script, "..")
sys.path.append(ruta_relativa)
from database import ConexionSybase
from conexiones import Conexion_APP
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

#conexion_sybase.eliminar_tabla("MPQRCODE_CONEXIONPROGRAMAS")
#conexion_sybase.crear_tabla_MPQRCODE_CONEXIONPROGRAMAS()
"""
datos = {
    "nro_factura": "00000-11111111",
    "tipo_factura": 1,
    "monto_pagar": 1000,
    "status": 0
}

conexion_sybase.insertar_datos_sin_obtener_id("MPQRCODE_CONEXIONPROGRAMAS", datos)
"""


"""
/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*LIMPIEZA/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*
instanciacion.limpieza_tabla_sucursal()
instanciacion.limpieza_tabla_caja()
"""
"""

instanciacion.eliminarCAJADBA()

instanciacion.limpieza_tabla_TOTALsucursal()
instanciacion.limpieza_tabla_TOTALcaja()
"""
instanciacion.eliminarOrdenesPostDBA()


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
"""
pago = instanciacion.crearOrden("SUC001POS001", "00000-1111111", "Changuito", 1000, "https://media.istockphoto.com/id/1205419959/es/vector/verduras-en-el-carro-de-la-compra-carrito-logotipo-icono-icono-vector-de-dise%C3%B1o.jpg?s=612x612&w=0&k=20&c=SFUApESf7KXEOLaVQrjUEihs0D8CJOy5nnqmDPQebGg=")
id_pago = instanciacion.obteneridOrder(pago[0], pago[1])
instanciacion.obtenerPago(id_pago, pago[0], pago[1])
"""
"""
datos = {
    'picture_url': "https://media.istockphoto.com/id/1205419959/es/vector/verduras-en-el-carro-de-la-compra-carrito-logotipo-icono-icono-vector-de-dise%C3%B1o.jpg?s=612x612&w=0&k=20&c=SFUApESf7KXEOLaVQrjUEihs0D8CJOy5nnqmDPQebGg="
}

conexion_sybase.actualizar_datos("MPQRCODE_CAJAS", datos, 1)
"""

#print(conexion_sybase.specify_search_condicion("MPQRCODE_SUCURSAL", 'name', 'external_id', 'SUC004'))
"""
conexion_sybase.eliminar_tabla("MPQRCODE_CLIENTE")
conexion_sybase.crear_tabla_MPQRCODE_CLIENTE()
"""
#conexion_sybase.eliminar_filas("MPQRCODE_SUCURSAL", "id", 59270546)


#respuesta1 = app.crear_ordenV2("SUC002", "SUC002POS001")

#respuesta1 = app.obtener_ordenV2("SUC002POS001")
#print(respuesta1)

#Crear Orden DINAMICO
#app.crear_orden_dinamico(1800, "Anonimo", "Ca_0101")

