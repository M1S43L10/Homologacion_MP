import os
import json
from flask import Flask, request

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        try:
            data = request.get_json()

            # Crear la carpeta "MERCHANT_ORDEN" si no existe
            if not os.path.exists('MERCHANT_ORDEN'):
                os.makedirs('MERCHANT_ORDEN')

            # Generar un nombre de archivo único basado en el ID del pedido (ajusta según tus necesidades)
            contador = 0
            if contador == 0:
                while contador < 2 :    
                    file_name = os.path.join('MERCHANT_ORDEN', f'order_{contador}.json')
                    contador = 1

            # Guardar los datos como un archivo JSON
            with open(file_name, 'w') as file:
                json.dump(data, file, indent=2)

            print(f"Datos recibidos y guardados en {file_name}")

            return 'OK'
        except Exception as e:
            print(f"Error al procesar la solicitud: {str(e)}")
            return 'Error', 500
    else:
        return 'HOLA SOY MISAEL'

if __name__ == '__main__':
    app.run(port=5000)
