from GUIPagoQR import InterfazMercadoPago
from Conexion_APIs_MP import Conexion_Api

"""if __name__ == "__main__":
    app = InterfazMercadoPago()
    app.mainloop()"""


app = Conexion_Api("1588285685", "APP_USR-3774512295656164-121208-e45df91faddd6fd608de107d1db2971f-1588285685")

#Crear Sucursal
#app.crear_sucursal("08:00", "13:00", "SUC002")

#Crear Caja
#app.crear_caja("Anonimo")

#Crear Orden ATENDIDO
#respuesta = app.crear_orden(1000, "SUC002POS001")
"""if respuesta >= 200 and respuesta < 300:
    respuesta1 = app.obtener_orden(91927793)
    while respuesta1 > 300 and respuesta1 < 500:
        respuesta1 = app.obtener_orden(91927793)
        print(respuesta1)"""

respuesta1 = app.obtener_orden(91927793)
print(respuesta1)

#Crear Orden DINAMICO
#app.crear_orden_dinamico(1800, "Anonimo", "Ca_0101")