# No es necesario agregar la ruta completa en sys.path
import sys
sys.path.append(r"C:\Users\Op_1111\Desktop\Codigos_GitHub\Homologacion_MP")

# Importa directamente desde Class_MP
from Class_MP.connect_db import ConexionSybase
from Class_MP.main import crear_ORDEN

from flask import Flask, request
app = Flask(__name__)

# Variable para almacenar el valor del ID de pago web
IDPAGOWEB = None

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
    global IDPAGOWEB  # Asegura que la variable sea tratada como global
    
    crear_ORDENweb = crear_ORDEN

    try:
        data = request.get_json()

        # Verifica si existe la clave "data" y su valor tiene la clave "id"
        if 'data' in data and 'id' in data['data']:
            IDPAGOWEB = data.get('IDPAGOWEB')  # Actualiza el valor de IDPAGOWEB si está presente en el POST
            conexion_sybase.actualizar_id_pago(crear_ORDENweb[0], IDPAGOWEB)
            print(f'IDPAGOWEB actualizado: {IDPAGOWEB}')

        return 'OK'
    except Exception as e:
        print(f"Error al procesar la solicitud: {str(e)}")
        return 'Error', 500

if __name__ == '__main__':
    app.run(port=5000)
