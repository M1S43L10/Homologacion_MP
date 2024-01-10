import requests
import json
import os

class Conexion_Api:
    def __init__(self, id_user, acess_token):
        self.id_user = id_user
        self.access_token = acess_token

    def crear_sucursal(self, datosSUC):
        # Url con el Id_User para crear la SUCURSAL
        url = f'https://api.mercadopago.com/users/{self.id_user}/stores'

        # Los headers que necesita la APIs para dar una respuesta
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {self.access_token}',  # Modificar los TOKENS de identificación de cada cuenta.
        }

        SUCload = datosSUC

        response = requests.post(url, headers=headers, data=json.dumps(SUCload))
        
        #GUARDAR EL JSON COMO ARCHIVO DE FORMAR LOCAL
        """
        # Crear la carpeta si no existe
        folder_path = "SUCURSALES_JSON"
        os.makedirs(folder_path, exist_ok=True)

        # Guardar la respuesta en un archivo JSON en la carpeta
        with open(os.path.join(folder_path, f"{direccion_SUC[7]}.json"), "w") as json_file:
            json.dump(response.json(), json_file, indent=2)
        """
        if response.status_code >= 200 and response.status_code < 300:
            print("Creación de Sucursal EXITOSA")
            return response
        else:
            print(f"No se logró la Conexión. {response.status_code}")


    def eliminar_sucursal(self, id_sucursal):
        try:
            url = f"https://api.mercadopago.com/users/{self.id_user}/stores/{id_sucursal}"

            headers = {
                'Content-Type': 'application/json',
                'Authorization': f'Bearer {self.access_token}',  # Modificar los TOKENS de identificación de cada cuenta.
            }

            # Realizar la solicitud para eliminar la sucursal
            response = requests.delete(url, headers=headers)
            return response.status_code
        except:
            print(response)

    def crear_caja(self, datosPOS):
        url = 'https://api.mercadopago.com/pos'

        hedears = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {self.access_token}'
        }

        POSload = datosPOS
        """
        {
            "category": int(datos_CAJA[0]),  # Convertir el conjunto a lista
            "external_id": str(datos_CAJA[1]),  # Asegurarse de que los datos sean strings si es necesario
            "external_store_id": external_store_id,
            "fixed_amount": True,
            "name": str(datos_CAJA[2]),
            "store_id": int(store_id)
        }

        """
        response = requests.post(url, headers=hedears, data=json.dumps(POSload))
        print(response)
        
        #CREAR ARCHIVO .JSON CON LA RESPUESTA Y GUARDARLO DE FORMA LOCAL (nombre_SUC)
        """# Crear la carpeta si no existe
        folder_path = f"{nombre_SUC}_CAJAS_JSON"
        os.makedirs(folder_path, exist_ok=True)

        # Guardar la respuesta en un archivo JSON en la carpeta
        with open(os.path.join(folder_path, f"{datos_CAJA[3]}.json"), "w") as json_file:
            json.dump(response.json(), json_file, indent=2)      
        """
        if response.status_code >= 200 and response.status_code < 300:
            print("Creación de Caja EXITOSA")
        else:
            print(f"No se logró la Conexión. ERROR {response.status_code} \t\n {response}")
            
        return response
    
    def eliminar_caja(self, idPOS):
        url = f"https://api.mercadopago.com/pos/{idPOS}"
        
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {self.access_token}'
        }
        
        response = requests.delete(url, headers=headers)
        
        return response.status_code
            
    #ORDEN ATENDIDA
    def crear_orden(self, external_id, factura, sucNAME, monto_pagar, picture_url):
        
        url = f"https://api.mercadopago.com/mpmobile/instore/qr/{self.id_user}/{external_id}"
        
        headers = {
            'Content-Type': 'application/json',
            'X-Ttl-Store-Preference': "180" ,
            'Authorization': f'Bearer {self.access_token}'
        }
        payload = {
            "external_reference": f"Factura-{factura}",
            "items": [
                {
                    'id': 000000000000,
                    'title': sucNAME,
                    'currency_id': "ARS",
                    'unit_price': monto_pagar,
                    'quantity': 1,
                    'description': "QR_ATENDIDO",
                    'picture_url': picture_url
                }
            ],
            "notification_url": "https://e0e7-186-122-104-145.ngrok-free.app/"
            }
        
        response = requests.post(url, headers=headers, data=json.dumps(payload))
        """
        # Crear la carpeta si no existe
        folder_path = "CREAR_PAGOS"
        os.makedirs(folder_path, exist_ok=True)

        # Guardar la respuesta en un archivo JSON en la carpeta
        with open(os.path.join(folder_path, f"{external_id}.json"), "w") as json_file:
            json.dump(response.json(), json_file, indent=2)
        print(response.status_code)
        """
        return response
    
    #NO FUNCIONA
    #CREAR LA ORDEN (VERSION 2.0) PODEMOS OBTENER LA ORDEN DE COMPRA
    def crear_ordenV2(self, external_store_id, external_pos_id):
        
        url = f"https://api.mercadopago.com/instore/qr/seller/collectors/{self.id_user}/stores/{external_store_id}/pos/{external_pos_id}/orders"    
        
        headers = {
            "Content-Type": 'application/json',
            'Authorization': f'Bearer {self.access_token}'
            }
        
        payload = {
            "cash_out": {
                "amount": 0
            },
            "description": "Purchase description.",
            "external_reference": "reference_12345",
            "items": [
                {
                "sku_number": "A123K9191938",
                "category": "marketplace",
                "title": "ANONIMO",
                "description": "SUPERMERCADO",
                "unit_price": 100,
                "quantity": 1,
                "unit_measure": "unit",
                "total_amount": 100
                },
            ],
            "notification_url": "https://www.yourserver.com/notifications",
            "title": "Product order",
            "total_amount": 100          
            }
        
        response = requests.put(url, headers=headers, data=json.dumps(payload))
        print(response)
        
    def obtener_ordenV2(self, external_pos_id,):
        url = f"https://api.mercadopago.com/instore/qr/seller/collectors/{self.id_user}/pos/{external_pos_id}/orders"
        
        headers = {
            "Content-Type": 'application/json',
            "Authorization": f"Bearer {self.access_token}"
            }
        
        response = requests.get(url= url, headers=headers)
        # Crear la carpeta si no existe
        folder_path = "OBTENER_PAGOS"
        os.makedirs(folder_path, exist_ok=True)

        # Guardar la respuesta en un archivo JSON en la carpeta
        with open(os.path.join(folder_path, f"{external_pos_id}.json"), "w") as json_file:
            json.dump(response.json(), json_file, indent=2)
        return response.status_code
    
        
        
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

        url = f"https://api.mercadopago.com/instore/orders/qr/seller/collectors/{self.id_user}/pos/{datos_diccionario['external_id']}/qrs"

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
                "title": "ANONIMO",
                "description": "SUPERMERCADO",
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
        return response   
    
    def obtener_pago(self, nro_operacion):
        url = f"https://api.mercadopago.com/v1/payments/{nro_operacion}"
        
        headers = {
            "Content-Type": 'application/json',
            'Authorization': f'Bearer {self.access_token}'
            }
        
        response = requests.get(url=url, headers=headers)
        """
        print(response.status_code)
        # Crear la carpeta si no existe
        folder_path = "OBTENER_PAGOS"
        os.makedirs(folder_path, exist_ok=True)

        # Guardar la respuesta en un archivo JSON en la carpeta
        with open(os.path.join(folder_path, f"{self.id_user}.json"), "w") as json_file:
            json.dump(response.json(), json_file, indent=2)
        print(response.status_code)
        """
        return response