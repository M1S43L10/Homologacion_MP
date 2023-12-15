import tkinter as tk
from Conexion_APIs_MP import Conexion_Api
from interfaz import Interfaz_MP_QR

app = Conexion_Api("1588285685", "APP_USR-3774512295656164-121208-e45df91faddd6fd608de107d1db2971f-1588285685")

#Crear Sucursal
#app.crear_sucursal("08:00", "13:00", "SUC002")

#Crear Caja
#app.crear_caja("Anonimo")

#Crear Orden ATENDIDO
app.crear_orden(15000, "SUC002POS001")

#Crear Orden DINAMICO
#app.crear_orden_dinamico(1800, "Anonimo", "Ca_0101")