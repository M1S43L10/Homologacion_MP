from flask import Flask, request
import json
import os
import sys
directorio_script = os.path.dirname(os.path.abspath(__file__))
# Construir la ruta relativa al directorio que deseas agregar
ruta_relativa = os.path.join(directorio_script, "..")
sys.path.append(ruta_relativa)
from database import ConexionSybase
import threading
from datetime import datetime, timedelta


# Obtener la fecha y hora actual
now = datetime.now()

# Calcular la fecha y hora hace 24 horas
twenty_four_hours_ago = now - timedelta(hours=24)

# Formatear las fechas
formato_fecha = now.strftime('%Y-%m-%d %H:%M:%S.%f')[:-3] 

app = Flask(__name__)

# Variable local para almacenar el valor de "id"
id_value = None
lock = threading.Lock()
# Configuración de Sybase
configuracion_sybase = {
    "user": "dba",
    "password": "gestion",
    "database": r"I:\Misa\tentollini_DBA 2023-12-11 12;05;28\Dba\gestionh.db",
    # Agrega otros parámetros según sea necesario
}

conexion_sybase = ConexionSybase(**configuracion_sybase)

@app.route('/', methods=['POST'])
def index():
    global id_value  # Asegura que las variables sean tratadas como globales
    dictPOST = None
    try:
        data = request.get_json()
        print("Received JSON:", data)  # Agrega esta línea para imprimir el JSON en la consola

        # Verifica si existe la clave "data" y su valor tiene la clave "id"
        if 'data' in data and 'id' in data['data']:
            id_increment = conexion_sybase.inicializar_tablas_OBTIENEidINCREMENT("MPQRCODE_RESPUESTAPOST", "action", data['action'])
            dict_valor = {}
            for clave_json, valor_json in data.items():  # Cambio aquí
                if clave_json == 'data':
                    dict_valor[clave_json] = valor_json['id']
                else:
                    dict_valor[clave_json] = valor_json
            conexion_sybase.actualizar_datos("MPQRCODE_RESPUESTAPOST", dict_valor, id_increment)
            print(dict_valor)
            print("AGREGADOS EN EL DBA")
        return 'OK'
    except Exception as e:
        print(f"Error al procesar la solicitud: {str(e)}")
        return 'Error', 500


if __name__ == '__main__':
    app.run(port=5000)

