import pypyodbc
import json


class ConexionSybase:
    def __init__(self, **kwargs):
        self.conexion = None
        self.cursor = None
        self.usuario = kwargs["user"]
        self.contrasena = kwargs["password"]
        self.base_datos = kwargs["database"]

    #CONEXION DE LA BASE DE DATOS
    def conectar(self):
        try:
            self.conexion = pypyodbc.connect(
                user=self.usuario,
                password=self.contrasena,
                database=self.base_datos,
                Driver="{Adaptive Server Anywhere 9.0}",
                DSN="GestionIH1111",  # Nombre del DSN configurado en tu sistema
                PWD=self.contrasena,
                FILE=self.base_datos,  # Ruta completa al archivo de base de datos
            )
            self.cursor = self.conexion.cursor()  # Crea el cursor
            return True
        except pypyodbc.Error as err:
            print(f"Error al conectar a Sybase: {err}")
            return False
        
        
    #MANEJO A LA BASE DE DATOS
    def eliminar_base_de_datos(self, nombre_bd):
        try:
            with self.conexion.cursor() as cursor:
                consulta = f"DROP DATABASE {nombre_bd}"
                cursor.execute(consulta)
                print(f"Base de datos '{nombre_bd}' eliminada exitosamente.")
        except pypyodbc.Error as err:
            print(f"Error al eliminar la base de datos: {err}")
            
        
    #MANEJOS DE TABLAS    
    def crear_tabla(self, nombre_tabla):
        try:
            self.conectar()
            query = f"""
                CREATE TABLE {nombre_tabla} (
                    ID INT IDENTITY PRIMARY KEY,
                    FECHA_CREACION DATETIME,
                    NRO_FACTURA VARCHAR(255),
                    PUNTO_VENTA VARCHAR(255),
                    FECHA_PAGO DATETIME,
                    ID_PAGO VARCHAR(255),
                )
            """
            self.cursor.execute(query)
            self.conexion.commit()
            print(f'Tabla {nombre_tabla} creada con éxito.')
        except Exception as e:
            print(f'Error al crear la tabla: {e}')
        finally:
            self.desconectar()

    def crear_tabla_MPQRCODE_SUCURSAL(self):
        try:
            self.conectar()
            query = """
                CREATE TABLE MPQRCODE_SUCURSAL (
                    idINCREMET INT IDENTITY PRIMARY KEY, 
                    id VARCHAR(255), 
                    name VARCHAR(255), 
                    date_creation VARCHAR(255),
                    external_id VARCHAR(255),
                )
            """
            self.cursor.execute(query)
            self.conexion.commit()
            print("Tabla MPQRCODE_SUCURSAL creada con éxito.")
        except Exception as e:
            print(f"Error al crear la tabla: {e}")
        finally:
            self.desconectar()
            
    def crear_tabla_MPQRCODE_SUCURSAL_business_hours(self):
        try:
            self.conectar()
            query = """
                CREATE TABLE MPQRCODE_SUCURSAL_business_hours (
                    idSUC VARCHAR(255),
                    DIA VARCHAR(255),
                    open_business_hours VARCHAR(255),
                    close_business_hours VARCHAR(255)                    
                )
            """
            self.cursor.execute(query)
            self.conexion.commit()
            print("Tabla MPQRCODE_SUCURSAL creada con éxito.")
        except Exception as e:
            print(f"Error al crear la tabla: {e}")
        finally:
            self.desconectar()
            
    def crear_tabla_MPQRCODE_SUCURSAL_location(self):
        try:
            self.conectar()
            query = """
                CREATE TABLE MPQRCODE_SUCURSAL_location (
                    idSUC VARCHAR(255),
                    address_line VARCHAR(255),
                    reference_location VARCHAR(255),
                    latitude FLOAT,
                    longitude FLOAT,
                    id VARCHAR(255),
                    type VARCHAR(255),
                    city VARCHAR(255),
                    state_id VARCHAR(255)                    
                )
            """
            self.cursor.execute(query)
            self.conexion.commit()
            print("Tabla MPQRCODE_SUCURSAL creada con éxito.")
        except Exception as e:
            print(f"Error al crear la tabla: {e}")
        finally:
            self.desconectar()
        
    
    def crear_tabla_MPQRCODE_CAJAS(self):
        try:
            self.conectar()
            query = """
                CREATE TABLE MPQRCODE_CAJAS (
                    idINCREMET INT IDENTITY PRIMARY KEY, 
                    id BIGINT, 
                    status VARCHAR(255), 
                    date_created VARCHAR(255), 
                    date_last_updated VARCHAR(255), 
                    uuid VARCHAR(255), 
                    user_id BIGINT, 
                    name VARCHAR(255), 
                    fixed_amount VARCHAR(255), 
                    category BIGINT, 
                    store_id VARCHAR(255), 
                    external_store_id VARCHAR(255), 
                    external_id VARCHAR(255), 
                    site VARCHAR(255), 
                    qr_code VARCHAR(255),
                ) 
            """
            self.cursor.execute(query)
            self.conexion.commit()
            print("Tabla MPQRCODE_CAJAS creada con éxito.")
        except Exception as e:
            print(f"Error al crear la tabla: {e}")
        finally:
            self.desconectar()
            
    def crear_tabla_MPQRCODE_CAJAS_qr(self):
        try:
            self.conectar()
            query = """
                CREATE TABLE MPQRCODE_CAJAS_qr (
                    id_POS BIGINT,
                    external_id VARCHAR(255),
                    image VARCHAR(255),
                    template_document VARCHAR(255),
                    template_image VARCHAR(255)
                )
            """
            self.cursor.execute(query)
            self.conexion.commit()
            print("Tabla MPQRCODE_CAJAS_qr creada con éxito.")
        except Exception as e:
            print(f"Error al crear la tabla: {e}")
        finally:
            self.desconectar()
            
    #----------------------------------------------------TABLAS QUE TRABAJAN JUNTOSA PARA LA OBTENCIÓN DEL PAGO----------------------------------------------------

    def crear_tabla_MPQRCODE_CREARORDEN(self):
        try:
            self.conectar()
            query = """
                CREATE TABLE MPQRCODE_CREARORDEN (
                    idINCREMET INT IDENTITY, 
                    date_creation DATETIME,
                    external_reference VARCHAR(255) PRIMARY KEY,
                    external_idPOS VARCHAR(255),
                    id BIGINT,
                    collector_id BIGINT, 
                    collector VARCHAR(255), 
                    total_amount BIGINT, 
                    amount BIGINT, 
                    operation_type VARCHAR(255),
                    marketplace VARCHAR(255), 
                    marketplace_fee VARCHAR(255), 
                    sponsor_id BIGINT, 
                    notification_url VARCHAR(255), 
                    expiration_date_to VARCHAR(255),                    
                    expires VARCHAR(255), 
                    additional_info VARCHAR(255), 
                    site_id VARCHAR(255), 
                    client_id BIGINT, 
                    processing_modes VARCHAR(255),
                )
            """
            self.cursor.execute(query)
            self.conexion.commit()
            print("Tabla MPQRCODE_CREARORDEN creada con éxito.")
        except Exception as e:
            print(f"Error al crear la tabla: {e}")
        finally:
            self.desconectar()
            
    def crear_tabla_MPQRCODE_CREARORDEN_items(self):
        try:
            self.conectar()
            query = """
                CREATE TABLE MPQRCODE_CREARORDEN_items (
                    external_reference VARCHAR(255),
                    idMERCADERIA VARCHAR(255),
                    category_id VARCHAR(255),
                    title VARCHAR(255),
                    quantity BIGINT,
                    currency_id VARCHAR(255),
                    unit_price FLOAT,
                    description VARCHAR(255),
                    picture_url VARCHAR(255)
                )
            """
            self.cursor.execute(query)
            self.conexion.commit()
            print("Tabla MPQRCODE_CREARORDEN creada con éxito.")
        except Exception as e:
            print(f"Error al crear la tabla: {e}")
        finally:
            self.desconectar()
            
    def crear_tabla_MPQRCODE_RESPUESTAPOST(self):
        try:
            self.conectar()
            query = """
                CREATE TABLE MPQRCODE_RESPUESTAPOST (
                    idINCREMET INT IDENTITY PRIMARY KEY, 
                    action VARCHAR(255), 
                    api_version VARCHAR(255), 
                    data VARCHAR(255), 
                    date_created VARCHAR(255), 
                    id BIGINT, 
                    live_mode VARCHAR(255), 
                    type VARCHAR(255), 
                    user_id VARCHAR(255)
                )
            """
            self.cursor.execute(query)
            self.conexion.commit()
            print("Tabla MPQRCODE_RESPUESTAPOST creada con éxito.")
        except Exception as e:
            print(f"Error al crear la tabla: {e}")
        finally:
            self.desconectar()
            
    def crear_tabla_MPQRCODE_OBTENERPAGO(self):
        try:
            self.conectar()
            query = """
                CREATE TABLE MPQRCODE_OBTENERPAGO (
                    idINCREMET INT IDENTITY PRIMARY KEY, 
                    accounts_info VARCHAR(255), 
                    acquirer_reconciliation VARCHAR(255), 
                    additional_info VARCHAR(255), 
                    authorization_code VARCHAR(255), 
                    binary_mode VARCHAR(255), 
                    brand_id VARCHAR(255), 
                    build_version VARCHAR(255), 
                    call_for_authorize_id VARCHAR(255), 
                    captured VARCHAR(255), 
                    card VARCHAR(255), 
                    charges_details VARCHAR(255), 
                    collector_id BIGINT, 
                    corporation_id VARCHAR(255), 
                    counter_currency VARCHAR(255), 
                    coupon_amount BIGINT, 
                    currency_id VARCHAR(255), 
                    date_approved VARCHAR(255), 
                    date_created VARCHAR(255), 
                    date_last_updated VARCHAR(255), 
                    date_of_expiration VARCHAR(255), 
                    deduction_schema VARCHAR(255), 
                    description VARCHAR(255), 
                    differential_pricing_id VARCHAR(255), 
                    external_reference VARCHAR(255), 
                    fee_details VARCHAR(255), 
                    financing_group VARCHAR(255), 
                    id BIGINT, 
                    installments INT, 
                    integrator_id VARCHAR(255), 
                    issuer_id VARCHAR(255), 
                    live_mode VARCHAR(255), 
                    marketplace_owner VARCHAR(255), 
                    merchant_account_id VARCHAR(255), 
                    merchant_number VARCHAR(255), 
                    metadata VARCHAR(255), 
                    money_release_date VARCHAR(255),
                    money_release_schema VARCHAR(255),
                    money_release_status VARCHAR(255), 
                    notification_url VARCHAR(255), 
                    operation_type VARCHAR(255), 
                    ordermp VARCHAR(255), 
                    payer VARCHAR(255), 
                    payment_method  VARCHAR(255), 
                    payment_method_id  VARCHAR(255), 
                    payment_type_id  VARCHAR(255), 
                    platform_id  VARCHAR(255), 
                    point_of_interaction  VARCHAR(255),
                    pos_id  VARCHAR(255), 
                    processing_mode  VARCHAR(255), 
                    refunds  VARCHAR(255), 
                    shipping_amount BIGINT, 
                    sponsor_id  VARCHAR(255), 
                    statement_descriptor VARCHAR(255), 
                    status  VARCHAR(255), 
                    status_detail  VARCHAR(255), 
                    store_id  VARCHAR(255), 
                    tags  VARCHAR(255), 
                    taxes_amount BIGINT, 
                    transaction_amount BIGINT, 
                    transaction_amount_refunded BIGINT, 
                    transaction_details VARCHAR(255)
                )
            """
            self.cursor.execute(query)
            self.conexion.commit()
            print("Tabla MPQRCODE_OBTENERPAGO creada con éxito.")
        except Exception as e:
            print(f"Error al crear la tabla: {e}")
        finally:
            self.desconectar()
            
    #CREAR EXEPCION PARA INSERTAR order del POST ya que en SyBase DICHA PALABRA ESTA RESERVA, EL valor de orden va a ir en ordermp

                
    def mostrar_tablas(self, nombre_bda):
        try:
            with self.conexion.cursor() as cursor:
                consulta = f"""
                    SELECT table_name
                    FROM {nombre_bda}..SYSTABLE
                """
                cursor.execute(consulta)
                filas = cursor.fetchall()

                print("Lista de tablas en la base de datos:")
                for fila in filas:
                    print(fila[0])
        except pypyodbc.Error as err:
            print(f"Error al mostrar las tablas: {err}")
    
    def actualizar_tabla(self, nombre_tabla, columnas_actualizadas):
        try:
            with self.conexion.cursor() as cursor:
                consulta = f"ALTER TABLE {nombre_tabla} {columnas_actualizadas}"
                cursor.execute(consulta)
                print(f"Tabla '{nombre_tabla}' actualizada exitosamente.")
        except pypyodbc.Error as err:
            print(f"Error al actualizar la tabla: {err}")
            
    def verificar_existencia_tabla(self, nombre_tabla):
        try:
            with self.conexion.cursor() as cursor:
                consulta = f"SELECT COUNT(*) FROM SYSTABLE WHERE TABLE_NAME = '{nombre_tabla}'"
                cursor.execute(consulta)
                cantidad = cursor.fetchone()[0]
                return cantidad > 0
        except pypyodbc.Error as err:
            print(f"Error al verificar la existencia de la tabla: {err}")
            return False


    def eliminar_tabla(self, nombre_tabla):
        try:
            if self.conectar():  # Llama a conectar antes de continuar
                if self.verificar_existencia_tabla(nombre_tabla):
                    with self.conexion.cursor() as cursor:
                        consulta = f"DROP TABLE {nombre_tabla}"
                        cursor.execute(consulta)
                        print(f"Tabla '{nombre_tabla}' eliminada exitosamente.")
                else:
                    print(f"La tabla '{nombre_tabla}' no existe en la base de datos.")
            else:
                print("Error al conectar a la base de datos.")
        except pypyodbc.Error as err:
            print(f"Error al eliminar la tabla: {err}")


            
    def limpiar_tabla(self, tabla):
        try:
            self.conectar()

            # Eliminar los datos de la tabla
            with self.conexion.cursor() as cursor:
                consulta_eliminar = f"DELETE FROM {tabla}"
                cursor.execute(consulta_eliminar)
                self.conexion.commit()

            print(f"Tabla '{tabla}' limpiada exitosamente.")
        except pypyodbc.Error as err:
            print(f"Error al limpiar la tabla: {err}")
        finally:
            self.desconectar()
            
    def seleccionar_tabla(self, nombre_tabla):
        try:
            with self.conexion.cursor() as cursor:
                consulta = f"SELECT * FROM {nombre_tabla}"
                cursor.execute(consulta)
                filas = cursor.fetchall()

                print(f"Contenido de la tabla '{nombre_tabla}':")
                for fila in filas:
                    print(fila)
        except pypyodbc.Error as err:
            print(f"Error al seleccionar la tabla '{nombre_tabla}': {err}")            

    # MANEJO DE DATOS DE UNA TABLA
    
    def insertar_dato_en_tabla(self, nombre_tabla, nombre_columna, id_increment, dato):
        try:
            self.conectar()

            # Verificar si la tabla existe en la base de datos
            if self.verificar_existencia_tabla(nombre_tabla):
                with self.conexion.cursor() as cursor:
                    # Verificar si la columna existe en la tabla
                    consulta_columna = f"SELECT COUNT(*) FROM SYS.SYSCOLUMNS WHERE tname = '{nombre_tabla}' AND cname = '{nombre_columna}'"
                    cursor.execute(consulta_columna)
                    existe_columna = cursor.fetchone()[0] > 0

                    if existe_columna:
                        # Verificar si existe una fila con el idINCREMET proporcionado
                        consulta_fila = f"SELECT COUNT(*) FROM {nombre_tabla} WHERE idINCREMET = {id_increment}"
                        cursor.execute(consulta_fila)
                        existe_fila = cursor.fetchone()[0] > 0

                        if existe_fila:
                            # Insertar el dato en la fila correspondiente
                            consulta_insertar = f"UPDATE {nombre_tabla} SET {nombre_columna} = '{dato}' WHERE idINCREMET = {id_increment}"
                            cursor.execute(consulta_insertar)
                            self.conexion.commit()

                            print(f"Dato '{dato}' insertado en la fila con idINCREMET={id_increment} en la tabla '{nombre_tabla}'.")
                        else:
                            # Insertar el dato en la fila correspondiente y establecer el idINCREMET
                            consulta_insertar = f"INSERT INTO {nombre_tabla} ({nombre_columna}) VALUES ('{dato}')"
                            cursor.execute(consulta_insertar)
                            self.conexion.commit()

                            # Obtener el idINCREMET recién asignado
                            consulta_id = f"SELECT @@IDENTITY"
                            cursor.execute(consulta_id)
                            id_increment_nuevo = cursor.fetchone()[0]

                            print(f"Dato '{dato}' insertado en la fila con idINCREMET={id_increment_nuevo} en la tabla '{nombre_tabla}'.")
                    else:
                        print(f"No existe la columna '{nombre_columna}' en la tabla '{nombre_tabla}'.")
            else:
                print(f"No existe la tabla '{nombre_tabla}' en la base de datos.")
        except pypyodbc.Error as err:
            print(f"Error al insertar dato en la tabla: {err}")
        finally:
            self.desconectar()



    
    
    def insertar_datos_obtener_idINCREMET(self, tabla, datos):
        try:
            self.conectar()
            with self.conexion.cursor() as cursor:
                # Construir la consulta SQL de inserción
                columnas = ", ".join([f'"{col}"' for col in datos.keys()])
                valores = ", ".join([f"'{v}'" if not isinstance(v, dict) else f"'{json.dumps(v)}'" for v in datos.values()])
                consulta_insert = f'INSERT INTO {tabla} ({columnas}) VALUES ({valores})'
                cursor.execute(consulta_insert)
                self.conexion.commit()

                # Obtener el valor autoincremental de la fila recién insertada
                consulta_id = f'SELECT @@IDENTITY'
                cursor.execute(consulta_id)
                id_increment_insertado = cursor.fetchone()[0]

                print(f"Datos insertados en la tabla '{tabla}' exitosamente. idINCREMET: {id_increment_insertado}")

                return id_increment_insertado
        except pypyodbc.Error as err:
            print(f"Error al insertar datos: {err}")
            return None
        finally:
            self.desconectar()

    def insertar_datos_sin_obtener_id(self, tabla, datos):
        try:
            self.conectar()
            with self.conexion.cursor() as cursor:
                # Construir la consulta SQL de inserción
                columnas = ", ".join([f'"{col}"' for col in datos.keys()])
                valores = ", ".join([f"'{v}'" if not isinstance(v, dict) else f"'{json.dumps(v)}'" for v in datos.values()])
                consulta_insert = f'INSERT INTO {tabla} ({columnas}) VALUES ({valores})'
                cursor.execute(consulta_insert)
                self.conexion.commit()

                print(f"Datos insertados en la tabla '{tabla}' exitosamente.")

        except pypyodbc.Error as err:
            print(f"Error al insertar datos: {err}")
        finally:
            self.desconectar()

#/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/ INSERTAR DATOS DE SUCURSAL #/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/
    def inicializar_tabla_MPQRCODE_SUCURSAL(self, id):
        datos = {
            'id': id
        }
        id_incrementado = self.insertar_datos_obtener_idINCREMET("MPQRCODE_SUCURSAL", datos)
        return id_incrementado

    def inicializar_tablas_OBTIENEIDINCREMET(self, tabla, columna_inicial ,datos_inicializar):
        datos = {
            columna_inicial: datos_inicializar
        }
        id_incrementado = self.insertar_datos_obtener_idINCREMET(tabla, datos)
        return id_incrementado
    
    def insertar_datos_MPQRCODE_SUCURSAL_business_hours(self, idSUC, dia, open, close):
        datos = {
            'idSUC' : idSUC,
            'DIA' : dia,
            'open_business_hours' : open,
            'close_business_hours' : close
        }        
        self.insertar_datos_sin_obtener_id("MPQRCODE_SUCURSAL_business_hours", datos)
        
    def insertar_datos_MPQRCODE_SUCURSAL_location(self, idSUC, address_line, reference, latitude, longitude, id_location, type_location, city, state_id):
        datos = {
            "idSUC" : idSUC,
            'address_line': address_line,
            'reference_location': reference,
            'latitude': latitude,
            'longitude': longitude,
            'id': id_location,
            'type': type_location,
            'city': city,
            'state_id': state_id
        }
        self.insertar_datos_sin_obtener_id("MPQRCODE_SUCURSAL_location", datos)
        
        
        
#/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/ INSERTAR DATOS DE CAJAS #/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/
    def inicializar_tabla_MPQRCODE_CAJAS(self, id):
        datos = {
            'id': id
        }
        id_incrementado = self.insertar_datos_obtener_idINCREMET("MPQRCODE_CAJAS", datos)
        return id_incrementado
    
    """
    def insertar_datos_MPQRCODE_CAJAS(self, id_POS, status, date_created, date_last_updated, uuid, user_id, name, fixed_amount, category, store_id, external_store_id, external_id, site, qr_code):
        datos = {
            'id' : id_POS,
            'status' : status,
            'date_created' : date_created,
            'date_last_updated': date_last_updated,
            'uuid' : uuid,
            'user_id': user_id,
            'name': name,
            'fixed_amount': fixed_amount,
            'category': category,
            'store_id': store_id,
            'external_store_id': external_store_id,
            'external_id': external_id,
            'site': site,
            'qr_code': qr_code            
        }
        self.insertar_datos_sin_obtener_id("MPQRCODE_CAJAS", datos)
        """
        
    def insertar_datos_MPQRCODE_CAJAS_qr(self, id_pos, image, template_document, template_image):
        datos = {
            'id_POS' : id_pos,
            'image': image,
            'template_document': template_document,
            'template_image': template_image
        }
        
        self.insertar_datos_sin_obtener_id("MPQRCODE_CAJAS_qr", datos)
        
    def insertar_datos_MPQRCODE_CAJAS_qrFALTANTE(self, external_id, id_POS):
        try:
            self.conectar()
            with self.conexion.cursor() as cursor:
                query = f"UPDATE MPQRCODE_CAJAS_qr SET external_id = '{external_id}' WHERE id_POS = '{id_POS}'"
                cursor.execute(query)
                self.conexion.commit()
                print("external_ID ACTUALIZADO")
        except pypyodbc.Error as err:
            print(f"Error al actualizar external_id: {err}")
        finally:
            self.desconectar()

    """
    #PRUEBAS QUE YA NO SE USAN
    def insertar_datos_MERCHANT(self, FECHA_CREACION, NRO_FACTURA, PUNTO_VENTA):
        datos = {
            'FECHA_CREACION': FECHA_CREACION,
            'NRO_FACTURA': NRO_FACTURA,
            'PUNTO_VENTA': PUNTO_VENTA
        }
        self.insertar_datos('MERCHANTORDEN', datos)
        
    def insertar_datos_MERCHANTPAGO(self, FECHA_CREACION, ID_PAGO):
        datos = {
            'FECHA_CREACION': FECHA_CREACION,
            'ID_PAGO': ID_PAGO,
        }
        self.insertar_datos('MERCHANTPAGO', datos)
    """            
    def actualizar_id_pago_MERCHANTORDEN(self, factura, POS, fecha_pago, ID_PAGO):
        try:
            self.conectar()

            # Verificar si existe una fila con la combinación de NRO_FACTURA y PUNTO_VENTA
            if self.existe_fila(factura, POS):
                with self.conexion.cursor() as cursor:
                    # Ejecutar la consulta para actualizar el ID_PAGO
                    query = f"UPDATE MERCHANTORDEN SET FECHA_PAGO = '{fecha_pago}', ID_PAGO = '{ID_PAGO}' WHERE NRO_FACTURA = '{factura}' AND PUNTO_VENTA = '{POS}'"
                    cursor.execute(query)
                    self.conexion.commit()

                    print(f"ID_PAGO actualizado exitosamente para la factura {POS}.")
            else:
                print(f"No se encontró una fila con NRO_FACTURA='{factura}' y PUNTO_VENTA='{POS}' en la base de datos.")
        except pypyodbc.Error as err:
            print(f"Error al actualizar ID_PAGO: {err}")
        finally:
            self.desconectar()
            
    def actualizar_hs_pago(self, factura, POS, fecha_creacion):
        try:
            self.conectar()

            # Verificar si existe una fila con la combinación de NRO_FACTURA y PUNTO_VENTA
            if self.existe_fila(factura, POS):
                with self.conexion.cursor() as cursor:
                    # Ejecutar la consulta para actualizar el ID_PAGO
                    query = f"UPDATE MERCHANTORDEN SET FECHA_CREACION = '{fecha_creacion}' WHERE NRO_FACTURA = '{factura}' AND PUNTO_VENTA = '{POS}'"
                    cursor.execute(query)
                    self.conexion.commit()

                    print(f"FECHA_CREACION actualizado exitosamente para la factura {POS}.")
            else:
                print(f"No se encontró una fila con NRO_FACTURA='{factura}' y PUNTO_VENTA='{POS}' en la base de datos.")
        except pypyodbc.Error as err:
            print(f"Error al actualizar FECHA_CREACION: {err}")
        finally:
            self.desconectar()

    def existe_fila(self, numero_factura, punto_venta):
        try:
            with self.conexion.cursor() as cursor:
                # Ejecutar la consulta para verificar la existencia de la fila
                query = f"SELECT 1 FROM MERCHANTORDEN WHERE NRO_FACTURA = '{numero_factura}' AND PUNTO_VENTA = '{punto_venta}'"
                cursor.execute(query)

                # Obtener el resultado de la consulta
                resultado = cursor.fetchone()

                # Si se encontró un resultado, la fila existe
                return resultado is not None
        except pypyodbc.Error as err:
            print(f"Error al verificar la existencia de la fila: {err}")
            return False

    
    # MANEJO DE OBTENCIOS DE DATOS DE UNA TABLA
    def obtener_id_compra(self, numero_factura, punto_venta):
        try:
            self.conectar()  # Asegúrate de conectar antes de ejecutar la consulta

            with self.conexion.cursor() as cursor:
                query = f"SELECT ID FROM MERCHANTORDEN WHERE NRO_FACTURA = '{numero_factura}' AND PUNTO_VENTA = '{punto_venta}'"
                cursor.execute(query)

                # Obtener el resultado de la consulta
                resultado_id_orden = cursor.fetchone()

                query = f"SELECT * FROM MERCHANTPAGO WHERE ID = '{resultado_id_orden[0]}'"
                cursor.execute(query)

                # Obtener el resultado de la consulta
                resultado = cursor.fetchone()
                
                if resultado is not None:
                    # Si se encontró un resultado, devolver el ID de compra y ID_PAGO
                    id_pago = resultado
                    print(f"ID_PAGO para factura {numero_factura} y POS {punto_venta}: {id_pago}")
                    return id_pago
                else:
                    # Si no se encontró ninguna coincidencia, devolver None
                    print(f"No se encontró una fila con NRO_FACTURA='{numero_factura}' y PUNTO_VENTA='{punto_venta}'.")
                    return None
        except pypyodbc.Error as err:
            print(f"Error al obtener el ID de compra: {err}")
            return None
        finally:
            self.desconectar()  # Asegúrate de desconectar incluso si hay un error

    def obtener_valor_id_por_idincremet(self, idincremet, nombre_tabla):
        try:
            self.conectar()
            with self.conexion.cursor() as cursor:
                # Consulta para obtener el valor de la columna 'id' por 'idINCREMET'
                query = f"SELECT id FROM {nombre_tabla} WHERE idINCREMET = {idincremet}"
                cursor.execute(query)
                resultado = cursor.fetchone()

                if resultado is not None:
                    id_valor = resultado[0]
                    print(f"Valor de 'id' para idINCREMET={idincremet}: {id_valor}")
                    return id_valor
                else:
                    print(f"No se encontró una fila con idINCREMET={idincremet}.")
                    return None
        except pypyodbc.Error as err:
            print(f"Error al obtener el valor de 'id': {err}")
            return None
        finally:
            self.desconectar()
            
    def obtener_valor_external_idPOS_por_idincremet(self, idincremet, nombre_tabla):
        try:
            self.conectar()
            with self.conexion.cursor() as cursor:
                # Consulta para obtener el valor de la columna 'id' por 'idINCREMET'
                query = f"SELECT external_id FROM {nombre_tabla} WHERE idINCREMET = {idincremet}"
                cursor.execute(query)
                resultado = cursor.fetchone()

                if resultado is not None:
                    id_valor = resultado[0]
                    print(f"Valor de 'external_id' para external_id={idincremet}: {id_valor}")
                    return id_valor
                else:
                    print(f"No se encontró una fila con external_id={idincremet}.")
                    return None
        except pypyodbc.Error as err:
            print(f"Error al obtener el valor de 'external_id': {err}")
            return None
        finally:
            self.desconectar()
            
    def obtener_valor_id_por_external_id(self, external_id, nombre_tabla):
        try:
            self.conectar()
            with self.conexion.cursor() as cursor:
                # Consulta para obtener el valor de la columna 'id' por 'external_id'
                query = f"SELECT id FROM {nombre_tabla} WHERE external_id = '{external_id}'"
                cursor.execute(query)
                resultado = cursor.fetchone()

                if resultado is not None:
                    id_valor = resultado[0]
                    print(f"Valor de 'id' para external_id={external_id}: {id_valor}")
                    return id_valor
                else:
                    print(f"No se encontró una fila con external_id={external_id}.")
                    return None
        except pypyodbc.Error as err:
            print(f"Error al obtener el valor de 'id': {err}")
            return None
            

#/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/ ELIMINAR DATOS DE CAJAS #/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/
    def eliminar_filas(self, tabla, columna, external_id):
        try:
            # Verifica si la conexión está establecida
            if not self.conexion:
                self.conectar()

            # Utiliza 'with' statement para asegurar el cierre adecuado del cursor
            with self.conexion.cursor() as cursor:
                # Construye y ejecuta la instrucción DELETE con parámetros de consulta
                sql_query = f"DELETE FROM {tabla} WHERE {columna} = '{external_id}'"
                print(f"Ejecutando SQL: {sql_query}")
                cursor.execute(sql_query)
                self.conexion.commit()

                print(f"Filas con external_id {external_id} eliminadas correctamente.")
        except pypyodbc.Error as err:
            print(f"Error: {err}")
        except Exception as e:
            print(f"Error: {e}")

    # DESCONECTAR DE LA BASE DE DATOS
    def desconectar(self):
        try:
            if self.conexion and self.conexion.connected:
                self.conexion.close()
                print("Conexión a Sybase cerrada.")
            else:
                print("La conexión ya estaba cerrada.")
        except pypyodbc.Error as err:
            print(f"Error al cerrar la conexión: {err}")


