def direccion_suc():
    nro_calle = input("Nro Calle:  ")
    nombre_calle = input("Calle: ")
    nombre_ciudad = input("Ciudad: ")
    nombre_provincia = input("Provincia: ")
    latitud = float(input("Latitud: "))
    longitud = float(input("Longitud: "))
    referencia = input("Referencia: ")
    nombre_SUC = input("Nombre de la Sucursal: ")
    return nro_calle, nombre_calle, nombre_ciudad, nombre_provincia, latitud, longitud, referencia, nombre_SUC

def datos_caja():
    categoria = int(input("Categoria: "))
    external_id = input("ID Externo: ")
    external_store_id = input("ID Tienda: ")
    name = input("Nombre Caja: ")
    return categoria, external_id, external_store_id, name