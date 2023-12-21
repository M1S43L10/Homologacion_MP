import os
import json
from flask import Flask, request
import threading
app = Flask(__name__)

responses = []
response_counter = 0
lock = threading.Lock()

@app.route('/', methods=['GET', 'POST'])
def index():
    global response_counter  # Asegura que response_counter sea tratada como una variable global

    if request.method == 'POST':
        try:
            data = request.get_json()

            # Bloquea el acceso a las variables compartidas
            with lock:
                responses.append(data)
                response_counter += 1

                # Si hemos recibido todas las respuestas, procesa y guarda
                if response_counter == 4:
                    # Restablece el contador para la próxima ronda de solicitudes
                    response_counter = 0

                    # Crear la carpeta "MERCHANT_ORDEN" si no existe
                    if not os.path.exists('MERCHANT_ORDEN'):
                        os.makedirs('MERCHANT_ORDEN')

                    # Guardar todas las respuestas como un solo archivo JSON
                    file_name = os.path.join('MERCHANT_ORDEN', 'all_responses.json')
                    with open(file_name, 'w') as file:
                        json.dump(responses, file, indent=2)

                    print(f"Todas las respuestas recibidas y guardadas en {file_name}")

            return 'OK'
        except Exception as e:
            print(f"Error al procesar la solicitud: {str(e)}")
            return 'Error', 500
    else:
        return 'HOLA SOY MISAEL'

if __name__ == '__main__':
    app.run(port=5000)
