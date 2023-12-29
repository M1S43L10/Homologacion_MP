class Conexion_APP():
    def __init__(self, conexionAPI, conexionDBA):
        self.conexionAPI = conexionAPI
        self.conexionDBA =  conexionDBA
        
        #/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/**/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/
        #UNION DE LAS CLASES Y FUNCIONES PARA LA CREACION DE SUCURSALES. Recorrer e insertar los datos
    def creacionSUC(self, external_IDSUC):
        try:
            MPQRCODE_RESPUESTA_SUCURSAL = self.conexionAPI.crear_sucursal("08:00", "13:00", external_IDSUC)
            variable_iniciadora = MPQRCODE_RESPUESTA_SUCURSAL["id"]
            nro_idINCREMET = self.conexionDBA.inicializar_tabla_MPQRCODE_SUCURSAL(variable_iniciadora)
            nombre_tabla = "MPQRCODE_SUCURSAL"

            # Recorre cada clave y valor en el JSON
            for clave_json, valor_json in MPQRCODE_RESPUESTA_SUCURSAL.items():
                if isinstance(valor_json, dict):
                    if clave_json == 'business_hours':
                        datos_business_hours = []
                        idSUC = self.conexionDBA.obtener_valor_id_por_idincremet(nro_idINCREMET, nombre_tabla)
                        for dia, horarios in valor_json.items():
                            datos_business_hours.append(dia)
                            for horario in horarios:
                                datos_business_hours.append(horario)
                            self.conexionDBA.insertar_datos_MPQRCODE_SUCURSAL_business_hours(idSUC, datos_business_hours[0], datos_business_hours[1]["open"], datos_business_hours[1]["close"])
                            datos_business_hours.clear()
                    elif clave_json == 'location':
                        datos_location = []
                        idSUC = self.conexionDBA.obtener_valor_id_por_idincremet(nro_idINCREMET, nombre_tabla)
                        for clave, valor in valor_json.items():
                            datos_location.append(valor)
                        self.conexionDBA.insertar_datos_MPQRCODE_SUCURSAL_location(idSUC, datos_location[0], datos_location[1], datos_location[2], datos_location[3], datos_location[4], datos_location[5], datos_location[6], datos_location[7])
                else:        
                    #Llama a la función insertar_dato_en_tabla con los parámetros correspondientes
                    self.conexionDBA.insertar_dato_en_tabla(nombre_tabla, clave_json, nro_idINCREMET, valor_json)
            print("Se guardar todos los datos en el BDA")
        except:
            print("ERROR EN LA CREACION DE LA SUCURSAL")
    
    def eliminarSUC(self, external_IDSUC):
        valor_idSUC = self.conexionDBA.obtener_valor_id_por_external_id(external_IDSUC, "MPQRCODE_SUCURSAL")
        respuesta = self.conexionAPI.eliminar_sucursal(valor_idSUC)
        if respuesta >= 200 and respuesta < 300:
            self.conexionDBA.eliminar_filas("MPQRCODE_SUCURSAL_location", "idSUC", int(valor_idSUC))
            self.conexionDBA.eliminar_filas("MPQRCODE_SUCURSAL_business_hours", "idSUC", int(valor_idSUC))
            self.conexionDBA.eliminar_filas("MPQRCODE_SUCURSAL", "id", int(valor_idSUC))
            self.conexionDBA.desconectar()
            print("SUCURSAL ELIMINADA")
        else:
            print("NO SE PUDO ELIMINAR LA SUCURSAL")
        

    
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
    def crearCaja(self, id_externoSUC):
        try:
            nombre_tabla = "MPQRCODE_CAJAS"
            #CREAR UNA VARIABLE EN EL CUAL SE PUEDA INGRESE EL external_id Y REEMPLAZARLAS en idSUC y MPQRCODE_RESPUESTA_CAJA
            idSUC = self.conexionDBA.obtener_valor_id_por_external_id(id_externoSUC, "MPQRCODE_SUCURSAL")
            MPQRCODE_RESPUESTA_CAJA = self.conexionAPI.crear_caja(id_externoSUC, idSUC)
            variable_iniciadora = MPQRCODE_RESPUESTA_CAJA["id"]
            nro_idINCREMET = self.conexionDBA.inicializar_tabla_MPQRCODE_CAJAS(variable_iniciadora)
                
            for clave_json, valor_json in MPQRCODE_RESPUESTA_CAJA.items():
                if isinstance(valor_json, dict):
                    if clave_json == "qr":
                        datos_qr = []
                        idPOS = self.conexionDBA.obtener_valor_id_por_idincremet(nro_idINCREMET, nombre_tabla)
                        for clave_qr, valor_qr in valor_json.items():
                            datos_qr.append(valor_qr)
                        self.conexionDBA.insertar_datos_MPQRCODE_CAJAS_qr(idPOS, datos_qr[0], datos_qr[1], datos_qr[2])
                else:
                    self.conexionDBA.insertar_dato_en_tabla(nombre_tabla, clave_json, nro_idINCREMET, valor_json)
            idPOS = self.conexionDBA.obtener_valor_id_por_idincremet(nro_idINCREMET, nombre_tabla)
            external_pos_id = self.conexionDBA.obtener_valor_external_idPOS_por_idincremet(nro_idINCREMET, nombre_tabla)
            self.conexionDBA.insertar_datos_MPQRCODE_CAJAS_qrFALTANTE(external_pos_id, idPOS)
            print("Se guardar todos los datos en el BDA")
                
        except:
            print("ERROR EN LA CREACION DE LA SUCURSAL")
            
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