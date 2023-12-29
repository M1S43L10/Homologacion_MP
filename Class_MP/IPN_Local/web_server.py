from flask import Flask, request
import sys
sys.path.append(r"C:\Users\Op_1111\Desktop\Codigos_GitHub\Homologacion_MP")
# Importa directamente desde Class_MP
from Class_MP.database import ConexionSybase
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

    try:
        data = request.get_json()
        # Verifica si existe la clave "data" y su valor tiene la clave "id"
        if 'data' in data and 'id' in data['data']:
            # Bloquea el acceso a la variable compartida
            with lock:
                id_value = data['data']['id']
                conexion_sybase.insertar_datos_MERCHANTPAGO(formato_fecha, id_value)
                print(f'VALOR ACTUALIZADO EN LA BASE DE DATOS')

        return 'OK'
    except Exception as e:
        print(f"Error al procesar la solicitud: {str(e)}")
        return 'Error', 500
if __name__ == '__main__':
    app.run(port=5000)
