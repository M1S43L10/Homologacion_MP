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
    name = input("Nombre Caja: ")
    return categoria, external_id, name

def dict_to_listaITEMS():
    id = int(input("ID del PRODUCTO: "))
    title = input("NOMBRE del PRODUCTO: ")
    currency_id = "ARS"
    unit_price = float(input("PRECIO del PRODUCTO: "))
    quantity = int(input("CANTIDAD del PRODUCTO: "))
    description = input("DESCRIPCIÓN del PRODUCTO: ")
    dictitem = {
        'id': id,
        'title': title,
        'currency_id': currency_id,
        'unit_price': unit_price,
        'quantity': quantity,
        'description': description
        #SOLUCIONAR PROBLEMA QUE NO CARGA IMG
    }
    return dictitem

def listaITEMS(supermercado, picture_url):
    cantidadITEMS = int(input("CANTIDAD DE PRODUCTOS: "))
    listITEMS = []
    dictitemDEFECTO = {
        'id': 0,
        'title': supermercado,
        'currency_id': "ARS",
        'unit_price': 0,
        'quantity': 1,
        'description': "NOMBRE DE LA SUCURSAL",
        'picture_url': picture_url
    }
    contador = 1
    listITEMS.append(dictitemDEFECTO)
    while contador <= cantidadITEMS:
        print(f"*/*/*/*/*/*/*/*/*/*/*/PRODUCTO {contador}*/*/*/*/*/*/*/*/*/*/*/")
        item = dict_to_listaITEMS()
        listITEMS.append(item)
        contador += 1
    print(listITEMS)
    return listITEMS