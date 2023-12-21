from GUIPagoQR import InterfazMercadoPago
from Conexion_APIs_MP import Conexion_Api
import os
import json




"""# Ejemplo de uso
if __name__ == "__main__":
    # Reemplaza los valores con la información correcta para tu conexión Sybase
    configuracion_sybase = {
        "user": "dba",
        "password": "gestion",
        "database": r"I:\Misa\tentollini_DBA 2023-12-11 12;05;28\Dba\gestionh.db",
        # Agrega otros parámetros según sea necesario
    }

    conexion_sybase = ConexionSybase(**configuracion_sybase)"""

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


crear_ORDEN = app.crear_orden(1000, "SUC002POS001", 1)

"""if crear_ORDEN >= 200 and crear_ORDEN < 300:
    # Procesar el archivo JSON recién creado
    file_path = os.path.join('IPN_Local', 'MERCHANT_ORDEN', 'all_responses.json')
    with open(file_path, 'r') as file:
        json_data = json.load(file)
        # Inicializar las variables para almacenar los valores de 'id'
        ids_data = []
        # Recorrer el archivo JSON y extraer los valores de 'id'
        for response in json_data:
            if 'data' in response:
                data = response['data']
                if 'id' in data:
                    ids_data.append(data['id'])
        obtener_PAGO = app.obtener_pago(ids_data[0])
        if obtener_PAGO  >= 200 and obtener_PAGO < 300:"""
            
#respuesta1 = app.crear_ordenV2("SUC002", "SUC002POS001")

#respuesta1 = app.obtener_ordenV2("SUC002POS001")
#print(respuesta1)

#Crear Orden DINAMICO
#app.crear_orden_dinamico(1800, "Anonimo", "Ca_0101")