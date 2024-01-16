import sys
import os
from Conexion_APIs_MP import Conexion_Api
from datetime import datetime, timedelta
import time

# Obtener la fecha y hora actual
now = datetime.now()

# Calcular la fecha y hora hace 24 horas
twenty_four_hours_ago = now - timedelta(hours=24)

# Formatear las fechas
formato_fecha = now.strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]  # Se omiten los últimos 3 caracteres para tener solo los milisegundos


class Conexion_APP():
    def __init__(self, conexionAPI, conexionDBA):
        self.conexionAPI = Conexion_Api(conexionAPI[0], conexionAPI[1])
        self.conexionDBA =  conexionDBA
        #/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/**/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/
        #UNION DE LAS CLASES Y FUNCIONES PARA LA CREACION DE SUCURSALES. Recorrer e insertar los datos
    def creacionSUC(self, datosSUC):
        try:
            response_MPQRCODE_RESPUESTA_SUCURSAL = self.conexionAPI.crear_sucursal(datosSUC)
            if response_MPQRCODE_RESPUESTA_SUCURSAL.status_code >= 200 and response_MPQRCODE_RESPUESTA_SUCURSAL.status_code < 300:
                MPQRCODE_RESPUESTA_SUCURSAL = response_MPQRCODE_RESPUESTA_SUCURSAL.json()
                variable_iniciadora = MPQRCODE_RESPUESTA_SUCURSAL["id"]
                nro_idINCREMENT = self.conexionDBA.inicializar_tabla_MPQRCODE_SUCURSAL(variable_iniciadora)
                nombre_tabla = "MPQRCODE_SUCURSAL"
                # Recorre cada clave y valor en el JSON
                for clave_json, valor_json in MPQRCODE_RESPUESTA_SUCURSAL.items():
                    if isinstance(valor_json, dict):
                        if clave_json == 'business_hours':
                            datos_business_hours = []
                            idSUC = self.conexionDBA.obtener_valor_id_por_idINCREMENT(nro_idINCREMENT, nombre_tabla)
                            for dia, horarios in valor_json.items():
                                datos_business_hours.append(dia)
                                for horario in horarios:
                                    datos_business_hours.append(horario)
                                self.conexionDBA.insertar_datos_MPQRCODE_SUCURSAL_business_hours(idSUC, datos_business_hours[0], datos_business_hours[1]["open"], datos_business_hours[1]["close"])
                                datos_business_hours.clear()
                        elif clave_json == 'location':
                            datos_location = []
                            idSUC = self.conexionDBA.obtener_valor_id_por_idINCREMENT(nro_idINCREMENT, nombre_tabla)
                            for clave, valor in valor_json.items():
                                datos_location.append(valor)
                            self.conexionDBA.insertar_datos_MPQRCODE_SUCURSAL_location(idSUC, datos_location[0], datos_location[1], datos_location[2], datos_location[3], datos_location[4], datos_location[5], datos_location[6], datos_location[7])
                    else:        
                        #Llama a la función insertar_dato_en_tabla con los parámetros correspondientes
                        self.conexionDBA.insertar_dato_en_tabla(nombre_tabla, clave_json, nro_idINCREMENT, valor_json)
                print("Se guardar todos los datos en el BDA")
                return response_MPQRCODE_RESPUESTA_SUCURSAL
        except Exception as e:
            print(f"ERROR EN LA CREACION DE LA SUCURSAL: {str(e)}")
            return response_MPQRCODE_RESPUESTA_SUCURSAL
    
    def eliminarSUC(self, external_IDSUC):
        valor_idSUC = self.conexionDBA.obtener_valor_id_por_external_id(external_IDSUC, "MPQRCODE_SUCURSAL")
        respuesta = self.conexionAPI.eliminar_sucursal(valor_idSUC)
        if respuesta >= 200 and respuesta < 300:
            self.conexionDBA.eliminar_filas("MPQRCODE_SUCURSAL_location", "idSUC", int(valor_idSUC))
            self.conexionDBA.eliminar_filas("MPQRCODE_SUCURSAL_business_hours", "idSUC", int(valor_idSUC))
            self.conexionDBA.eliminar_filas("MPQRCODE_SUCURSAL", "id", int(valor_idSUC))
            self.conexionDBA.desconectar()
            print("SUCURSAL ELIMINADA")
            return True
        else:
            print("NO SE PUDO ELIMINAR LA SUCURSAL")
            return False, respuesta
        

    
    def limpieza_tabla_TOTALsucursal(self):
        self.conexionDBA.eliminar_tabla("MPQRCODE_SUCURSAL")
        self.conexionDBA.eliminar_tabla("MPQRCODE_SUCURSAL_business_hours")
        self.conexionDBA.eliminar_tabla("MPQRCODE_SUCURSAL_location")
        self.conexionDBA.crear_tabla_MPQRCODE_SUCURSAL()
        self.conexionDBA.crear_tabla_MPQRCODE_SUCURSAL_business_hours()
        self.conexionDBA.crear_tabla_MPQRCODE_SUCURSAL_location()
    
    def limpieza_tabla_sucursal(self):
        self.conexionDBA.limpiar_tabla("MPQRCODE_SUCURSAL")
        self.conexionDBA.limpiar_tabla("MPQRCODE_SUCURSAL_business_hours")
        self.conexionDBA.limpiar_tabla("MPQRCODE_SUCURSAL_location")
    

    #/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/**/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/
    #UNION DE LAS CLASES Y FUNCIONES PARA LA CREACION DE LAS CAJAS PARA LAS SUCURSALES. Recorrer e insertar los datos
    def crearCaja(self, id_externoSUC, datosLISTPOS, picture__url):
        try:
            nombre_tabla = "MPQRCODE_CAJAS"
            #CREAR UNA VARIABLE EN EL CUAL SE PUEDA INGRESE EL external_id Y REEMPLAZARLAS en idSUC y MPQRCODE_RESPUESTA_CAJA
            idSUC = self.conexionDBA.obtener_valor_id_por_external_id(id_externoSUC, "MPQRCODE_SUCURSAL")
            datosPOS = {
                "category": int(datosLISTPOS[0]),  # Convertir el conjunto a lista
                "external_id": str(datosLISTPOS[1]),  # Asegurarse de que los datos sean strings si es necesario
                "external_store_id": id_externoSUC,
                "fixed_amount": True,
                "name": str(datosLISTPOS[2]),
                "store_id": int(idSUC),
            }
            MPQRCODE_RESPUESTA_CAJA = self.conexionAPI.crear_caja(datosPOS)
            MPQRCODE_RESPUESTA_CAJA_JSON = MPQRCODE_RESPUESTA_CAJA.json()
            print(MPQRCODE_RESPUESTA_CAJA_JSON)
            if MPQRCODE_RESPUESTA_CAJA.status_code >= 200 and MPQRCODE_RESPUESTA_CAJA.status_code < 300:
                variable_iniciadora = MPQRCODE_RESPUESTA_CAJA_JSON["id"]
                nro_idINCREMENT = self.conexionDBA.inicializar_tabla_MPQRCODE_CAJAS(variable_iniciadora)
                picture__urldatos = {
                    'external_store_id': id_externoSUC,
                    'picture_url': picture__url
                }
                self.conexionDBA.actualizar_datos("MPQRCODE_CAJAS", picture__urldatos, nro_idINCREMENT)
                for clave_json, valor_json in MPQRCODE_RESPUESTA_CAJA_JSON.items():
                    if isinstance(valor_json, dict):
                        if clave_json == "qr":
                            datos_qr = []
                            idPOS = self.conexionDBA.obtener_valor_id_por_idINCREMENT(nro_idINCREMENT, nombre_tabla)
                            for clave_qr, valor_qr in valor_json.items():
                                datos_qr.append(valor_qr)
                            self.conexionDBA.insertar_datos_MPQRCODE_CAJAS_qr(idPOS, datos_qr[0], datos_qr[1], datos_qr[2])
                    else:
                        self.conexionDBA.insertar_dato_en_tabla(nombre_tabla, clave_json, nro_idINCREMENT, valor_json)
                idPOS = self.conexionDBA.obtener_valor_id_por_idINCREMENT(nro_idINCREMENT, nombre_tabla)
                external_pos_id = self.conexionDBA.obtener_valor_external_idPOS_por_idINCREMENT(nro_idINCREMENT, nombre_tabla)
                self.conexionDBA.insertar_datos_MPQRCODE_CAJAS_qrFALTANTE(external_pos_id, idPOS)
                print("Se guardar todos los datos en el BDA")
                return MPQRCODE_RESPUESTA_CAJA
            else:
                return MPQRCODE_RESPUESTA_CAJA_JSON
        
        #DEFINIR BIEN LA LOGICA CON GUICrearCaja.py
        except Exception as e:
            print(f"ERROR EN LA CREACION DE LA SUCURSAL: {e}")
            return MPQRCODE_RESPUESTA_CAJA_JSON
            
    def eliminarCaja(self, valor_external_id):
        valor_idPOS = self.conexionDBA.obtener_valor_id_por_external_id(valor_external_id, "MPQRCODE_CAJAS")
        respuesta = self.conexionAPI.eliminar_caja(valor_idPOS)
        if respuesta >= 200 and respuesta < 300:
            self.conexionDBA.eliminar_filas("MPQRCODE_CAJAS_qr", "id_POS", valor_idPOS)
            self.conexionDBA.eliminar_filas("MPQRCODE_CAJAS", "id", valor_idPOS)
            self.conexionDBA.desconectar()
            print(f"CAJA {valor_external_id}: ELIMINADA")
        else:
            print("NO SE PUDO ELIMINAR LA CAJA")            
    
    def limpieza_tabla_TOTALcaja(self):
        self.conexionDBA.eliminar_tabla("MPQRCODE_CAJAS")
        self.conexionDBA.eliminar_tabla("MPQRCODE_CAJAS_qr")
        self.conexionDBA.crear_tabla_MPQRCODE_CAJAS()
        self.conexionDBA.crear_tabla_MPQRCODE_CAJAS_qr()
    
    def limpieza_tabla_caja(self):
        self.conexionDBA.limpiar_tabla("MPQRCODE_CAJAS")
        self.conexionDBA.limpiar_tabla("MPQRCODE_CAJAS_qr")
        
        #/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/**/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/
        #UNIÓN PARA CREAR ORDENES
    def crearOrden(self, external_idPOS, nro_factura, sucNAME, monto_pagar, picture_url):
        tabla = 'MPQRCODE_CREARORDEN'
        crear_ORDEN = self.conexionAPI.crear_orden(external_idPOS, nro_factura, sucNAME, monto_pagar, picture_url)
        print(crear_ORDEN)
        if crear_ORDEN.status_code >= 200 and crear_ORDEN.status_code < 300:
            external_reference = None
            for clave_json, valor_json in crear_ORDEN.json().items():
                if clave_json == 'external_reference':
                    external_reference = valor_json
                else:
                    pass
            valor1 = {
                'external_reference' : external_reference,
                'date_creation': formato_fecha
            }
            id_increment = self.conexionDBA.insertar_datos_obtener_idINCREMENT(tabla, valor1)
            self.conexionDBA.insertar_dato_en_tabla(tabla, 'external_idPOS', id_increment, external_idPOS)
            try:
                valor_DICT = {}
                for clave_json, valor_json in crear_ORDEN.json().items():
                    if clave_json == 'items' and isinstance(valor_json, list):
                        # Tu código aquí si clave_json es 'items' y valor_json es una lista
                        for recorre_lista in valor_json:
                            valor_dictITEMS = {}
                            for clave_dict, valor_dict in recorre_lista.items():
                                if clave_dict == 'id':
                                    valor_dictITEMS['external_reference'] = external_reference
                                    valor_dictITEMS['idMERCADERIA'] = valor_dict
                                else:
                                    valor_dictITEMS[clave_dict] = valor_dict
                            self.conexionDBA.insertar_datos_sin_obtener_id("MPQRCODE_CREARORDEN_items", valor_dictITEMS)
                            print(valor_dictITEMS)
                    elif not isinstance(valor_json, (list, dict)) and not clave_json == 'external_reference':
                        valor_DICT[clave_json] = valor_json
                    else:
                        pass
                self.conexionDBA.actualizar_datos(tabla, valor_DICT, id_increment)
                return external_reference, external_idPOS
            except Exception as e:
                print(f"Error: {e}")
                # Manejo de errores o cualquier otra acción necesaria
            finally:
                self.conexionDBA.desconectar()
                
    def obteneridOrder(self, external_reference, external_idPOS):
        obtener_ID = None
        while obtener_ID is None:
            obtener_ID = self.conexionDBA.obtener_id_compra(external_reference, external_idPOS)            
            if obtener_ID is None:
                print("Esperando confirmación del pago...")
                time.sleep(5)  # Puedes ajustar el tiempo de espera según sea necesario
        print("Pago Realizado. ID obtenido:", obtener_ID[0])
        return obtener_ID[0], True
        
    def obtenerPago(self, id_pago, external_reference, external_idPOS):
        print("BUSCANDO STATUS DEL PAGO: ")
        datos = {
            'external_reference': external_reference,
            'external_idPOS': external_idPOS
        }
        id_increment = self.conexionDBA.insertar_datos_obtener_idINCREMENT("MPQRCODE_OBTENERPAGO", datos)

        # Asegúrate de que obtienes la respuesta correctamente
        respuesta = self.conexionAPI.obtener_pago(id_pago)

        try:
            # Verifica si la respuesta es un objeto JSON válido
            json_response = respuesta.json()
        except ValueError as e:
            print(f"Error al parsear la respuesta JSON: {str(e)}")
            return

        datos = {}

        for clave_json, valor_json in json_response.items():
            if clave_json == 'order' and isinstance(valor_json, dict):
                for recorre_dict, valordict in valor_json.items():
                    if recorre_dict == 'id':
                        datos['order_id'] = valordict
                    else:
                        datos['order_type'] = valordict
            elif clave_json == 'payer' and isinstance(valor_json, dict):
                for recorre_dict, valordict in valor_json.items():
                    if recorre_dict == 'id':
                        datos['payer_id'] = valordict
                    else:
                        print("Se encontró una respuesta no esperada.")
            elif clave_json == 'payment_method' and isinstance(valor_json, dict):
                for recorre_dict, valordict in valor_json.items():  # Corregir aquí a valordict
                    if recorre_dict == 'id':
                        datos['payment_metodo_id'] = valordict
                    elif recorre_dict == 'issuer_id':
                        datos['payment_metodo_issuer_id'] = valordict
                    else:
                        datos['payment_metodo_type'] = valordict
            elif clave_json == 'transaction_details' and isinstance(valor_json, dict):
                for recorre_dict, valordict in valor_json.items():  # Corregir aquí a valordict
                    if recorre_dict == 'total_paid_amount':
                        datos['transaction_details_total_paid_amount'] = valordict
                    else:
                        pass
            else:
                columnas = self.conexionDBA.obtener_nombres_columnas("MPQRCODE_OBTENERPAGO")
                for colum_name in columnas:
                    if clave_json == colum_name and not clave_json == 'external_reference':
                        datos[clave_json] = valor_json
                    else:
                        pass
        self.conexionDBA.actualizar_datos("MPQRCODE_OBTENERPAGO", datos, id_increment)
        status = self.conexionDBA.specify_search("MPQRCODE_OBTENERPAGO", 'status', id_increment)
        status_detail = self.conexionDBA.specify_search("MPQRCODE_OBTENERPAGO", 'status_detail', id_increment)
        if status == 'approved' and status_detail == 'accredited':
            print("PAGO REALIZADO")
            return True
        else:
            print("NO SE PUDO OBTENER EL PAGO")
            return False
            
            
    def crearOrdenFULL(self, external_id_pos, nroFactura, sucNAME, montoPagar, pictureURL):
        pago = self.crearOrden(external_id_pos, nroFactura, sucNAME, montoPagar, pictureURL)
        id_pago = self.obteneridOrder(pago[0], pago[1])
        respuesta = self.obtenerPago(id_pago, pago[0], pago[1])
        return respuesta
                
            
    def eliminarOrdenesPostDBA(self):
        try:
            self.conexionDBA.eliminar_tabla("MPQRCODE_CREARORDEN")
            self.conexionDBA.eliminar_tabla("MPQRCODE_CREARORDEN_items")
            self.conexionDBA.eliminar_tabla("MPQRCODE_RESPUESTAPOST")
            self.conexionDBA.eliminar_tabla("MPQRCODE_OBTENERPAGO")
            self.conexionDBA.crear_tabla_MPQRCODE_CREARORDEN()
            self.conexionDBA.crear_tabla_MPQRCODE_CREARORDEN_items()
            self.conexionDBA.crear_tabla_MPQRCODE_RESPUESTAPOST()
            self.conexionDBA.crear_tabla_MPQRCODE_OBTENERPAGO()
        except Exception as e:
            print(f"Eror: {e}")
            
    def eliminarCAJADBA(self):
        try:
            self.conexionDBA.eliminar_tabla("MPQRCODE_CAJA")
            self.conexionDBA.crear_tabla_MPQRCODE_CAJA()
        except Exception as e:
            print(f"Eror: {e}")
