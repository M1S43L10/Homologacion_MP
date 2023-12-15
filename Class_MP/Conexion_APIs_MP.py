import requests
import json
import os
from direccion import *
import tkinter as tk
from PIL import Image, ImageTk
from qrcode.main import QRCode

class Conexion_Api:
    def __init__(self, id_user, acess_token):
        self.id_user = id_user
        self.access_token = acess_token

    def crear_sucursal(self, hs_abrir, hs_cerrar, nro_sucursal):
        # Url con el Id_User para crear la SUCURSAL
        url = f'https://api.mercadopago.com/users/{self.id_user}/stores'

        # Los headers que necesita la APIs para dar una respuesta
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {self.access_token}',  # Modificar los TOKENS de identificación de cada cuenta.
        }

        # Función que pide los datos de la Sucursal
        direccion_SUC = direccion_suc()

        SUCload = {
            'business_hours': {
                'monday': [
                    {
                        'open': f'{hs_abrir}',
                        'close': f'{hs_cerrar}',
                    },
                ],
                'tuesday': [
                    {
                        'open': f'{hs_abrir}',
                        'close': f'{hs_cerrar}',
                    },
                ],
            },
            'external_id': f'{nro_sucursal}',  # Asignar el id como se identificara a la sucursal para mas adelante
            'location': {
                'street_number': direccion_SUC[0],
                'street_name': direccion_SUC[1],
                'city_name': direccion_SUC[2],
                'state_name': direccion_SUC[3],
                'latitude': direccion_SUC[4],
                'longitude': direccion_SUC[5],
                'reference': direccion_SUC[6],
            },
            'name': direccion_SUC[7],
        }

        response = requests.post(url, headers=headers, data=json.dumps(SUCload))

        # Crear la carpeta si no existe
        folder_path = "SUCURSALES_JSON"
        os.makedirs(folder_path, exist_ok=True)

        # Guardar la respuesta en un archivo JSON en la carpeta
        with open(os.path.join(folder_path, f"{direccion_SUC[7]}.json"), "w") as json_file:
            json.dump(response.json(), json_file, indent=2)

        if response.status_code >= 200 and response.status_code < 300:
            print("Creación de Sucursal EXITOSA")
        else:
            print("No se logró la Conexión.")


    def eliminar_sucursal(self, id_sucursal, nombre_SUC):
        url = f"https://api.mercadopago.com/users/{self.id_user}/stores/{id_sucursal}"

        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {self.access_token}',  # Modificar los TOKENS de identificación de cada cuenta.
        }

        # Realizar la solicitud para eliminar la sucursal
        response = requests.delete(url, headers=headers)

        if response.status_code >= 200 and response.status_code < 300:
            print(f"Eliminación de Sucursal EXITOSA {response.status_code}")

            # Eliminar el archivo JSON correspondiente a la sucursal
            folder_path = "SUCURSALES_JSON"
            json_file_path = os.path.join(folder_path, f"{nombre_SUC}.json")
            

            #IF A ELIMINAR
            if os.path.exists(json_file_path):
                os.remove(json_file_path)
                print(f"Archivo JSON de la Sucursal {id_sucursal} eliminado.")
            else:
                print(f"Archivo JSON de la Sucursal {id_sucursal} no encontrado.")
        else:
            print("No se logró la Conexión.")

    def crear_caja(self, nombre_SUC):
        url = 'https://api.mercadopago.com/pos'

        hedears = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {self.access_token}'
        }

        datos_CAJA = datos_caja()

        POSload = {
            "category": int(datos_CAJA[0]),  # Convertir el conjunto a lista
            "external_id": str(datos_CAJA[1]),  # Asegurarse de que los datos sean strings si es necesario
            "external_store_id": str(datos_CAJA[2]),
            "fixed_amount": True,
            "name": str(datos_CAJA[3])
        }


        response = requests.post(url, headers=hedears, data=json.dumps(POSload))
        print(response)
        # Crear la carpeta si no existe
        folder_path = f"{nombre_SUC}_CAJAS_JSON"
        os.makedirs(folder_path, exist_ok=True)

        # Guardar la respuesta en un archivo JSON en la carpeta
        with open(os.path.join(folder_path, f"{datos_CAJA[3]}.json"), "w") as json_file:
            json.dump(response.json(), json_file, indent=2)
        

        if response.status_code >= 200 and response.status_code < 300:
            print("Creación de Caja EXITOSA")
        else:
            print("No se logró la Conexión.")
            
    #def eliminar_caja(self):
    
    def crear_orden(self, precio, external_id):
        
        url = f"https://api.mercadopago.com/mpmobile/instore/qr/{self.id_user}/{external_id}"
        
        headers = {
            'Content-Type': 'application/json',
            'X-Ttl-Store-Preference': "180" ,
            'Authorization': f'Bearer {self.access_token}'
        }
        payload = {
            "external_reference": "Factura-0001",
            "items": [
                {
                "id": 78123172,
                "title": "CHANGUITO",
                "currency_id": "ARG",
                "unit_price": precio,
                "quantity": 1,
                "description": "MERCADERIAS",
                "picture_url": "https://previews.123rf.com/images/freaktor/freaktor2002/freaktor200200004/139383340-verduras-en-carro-de-compras-carro-supermercado-logo-icono-dise%C3%B1o-vector.jpg"
                },
            ]
            }
        
        response = requests.post(url, headers=headers, data=json.dumps(payload))
        print(response)
        
    def crear_orden_dinamico(self, precio ,nombre_SUC, nombre_CAJA):

        # Obtener la ruta del directorio de trabajo actual
        directorio_de_trabajo = os.getcwd()

        # Ruta relativa de la carpeta "CAJAS_JSON"
        carpeta_cajas_json = os.path.join(directorio_de_trabajo, f"{nombre_SUC}_CAJAS_JSON")

        # Ruta relativa del archivo "Op_0101" dentro de la carpeta
        archivo_json = os.path.join(carpeta_cajas_json, f"{nombre_CAJA}.json")

        datos_diccionario = {}

        # Verificar si la carpeta existe
        if os.path.exists(carpeta_cajas_json):
            # Verificar si el archivo existe
            if os.path.isfile(archivo_json):
                # Abrir el archivo
                with open(archivo_json, 'r') as archivo:
                    contenido = archivo.read()
                    datos_diccionario = json.loads(contenido)
                    #print(json.dumps(datos_diccionario, indent=4, sort_keys=True))
            else:
                print(f"El archivo {archivo_json} no existe.")
        else:
            print(f"La carpeta {carpeta_cajas_json} no existe.")

        url  = f"https://api.mercadopago.com/instore/orders/qr/seller/collectors/{self.id_user}/pos/{datos_diccionario["external_id"]}/qrs"

        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {self.access_token}'
        }

        pagodata_json = {
            "cash_out": {
                "amount": 0
            },
            "description": "Purchase description.",
            "external_reference": "reference_12345",
            "items": [
                {
                "sku_number": "A123K9191938",
                "category": "marketplace",
                "title": "CHANGUITO",
                "description": "This is the Point Mini",
                "unit_price": precio,
                "quantity": 1,
                "unit_measure": "unit",
                "total_amount": precio
                },
            ],
            "notification_url": "https://www.yourserver.com/notifications",
            "title": "Product order",
            "total_amount": precio          
            }
        
        response = requests.post(url, headers=headers, data=json.dumps(pagodata_json))
        # Simula la obtención del código QR (reemplaza esto con tu código real)
        json_data = response.json()
        print(json_data)
        qr_data = json_data['qr_data']
        print(qr_data)

        # Crear el código QR con un tamaño más pequeño
        qr = QRCode(version=3, box_size=8.5 , border=2)
        qr.add_data(str(qr_data))
        qr.make(fit=True)

        # Crear la imagen del código QR directamente
        img = qr.make_image(fill_color=(0, 0, 0), back_color=(255, 255, 255))

        # Crear una ventana Tkinter con un tamaño más pequeño
        ventana = tk.Tk()
        ventana.title("Código QR")

        # Convertir la imagen del código QR a un objeto PhotoImage de Tkinter
        imagen_tk = ImageTk.PhotoImage(img)

        # Crear un widget Label para mostrar la imagen
        etiqueta = tk.Label(ventana, image=imagen_tk)
        etiqueta.pack(padx=5, pady=5)  # Ajusta el espacio alrededor de la imagen

        # Establecer el tamaño de la ventana
        ventana.geometry("400x400")  # Ajusta el tamaño de la ventana según tus necesidades

        # Ejecutar el bucle de eventos de Tkinter
        ventana.mainloop()
        