
import sys
import os
import tkinter as tk
from tkinter import ttk, simpledialog, messagebox
from getpass import getpass
from GUICrearSucursal import CrearSucursalApp
from GUICrearCaja import CrearCajaApp
from GUICrearOrden import CrearOrdenApp
from GUIConfigCaja import ConfigurarCajaApp
directorio_script = os.path.dirname(os.path.abspath(__file__))
# Construir la ruta relativa al directorio que deseas agregar
ruta_relativa = os.path.join(directorio_script, "..")
sys.path.append(ruta_relativa)
from database import ConexionSybase
from conexiones import Conexion_APP

class ConfigInicialMPQRCODE:
    def __init__(self):
        self.user_id = None
        self.access_token = None
        self.conexionDBA = ConexionSybase(
            user="dba",
            password="gestion",
            database=r"I:\Misa\tentollini_DBA 2023-12-11 12;05;28\Dba\gestionh.db",
        )
        self.validar_password()

    def validar_password(self):
        try:
            password_ingresado = simpledialog.askstring("Password", "Ingrese el password:", show='*')
            password_correcto = "***"

            if password_ingresado == password_correcto:
                if self.tabla_clientes_vacia():
                    self.crear_interfaz()
                    messagebox.showinfo("Información", "Cliente cargado.")
                    gui_conexiones = GUIconexiones(self.conexionDBA)
                    gui_conexiones.crear_ventana_principal()
                else:
                    messagebox.showinfo("Información", "Ya hay un cliente cargado.")
                    gui_conexiones = GUIconexiones(self.conexionDBA)
                    gui_conexiones.crear_ventana_principal()
            else:
                messagebox.showerror("Error", "Password incorrecto.")
        except Exception as e:
            messagebox.showerror("Error", f"Error: {str(e)}")

    def tabla_clientes_vacia(self):
        try:
            return self.conexionDBA.contar_registros("MPQRCODE_CLIENTE") == 0
        except Exception as e:
            messagebox.showerror("Error", f"Error al contar registros: {str(e)}")

    def crear_interfaz(self):
        self.root = tk.Tk()
        self.root.title("Configuración inicial MPQRCODE")

        style = ttk.Style()
        style.theme_use('xpnative')

        ttk.Label(self.root, text="User ID de MercadoPago:").grid(row=0, column=0, padx=10, pady=5, sticky='w')
        ttk.Label(self.root, text="Access Token de MercadoPago:").grid(row=1, column=0, padx=10, pady=5, sticky='w')

        self.entry_user_id = ttk.Entry(self.root, font=('Helvetica', 12))
        self.entry_access_token = ttk.Entry(self.root, show='*', font=('Helvetica', 12))

        self.entry_user_id.grid(row=0, column=1, padx=10, pady=5, sticky='ew')
        self.entry_access_token.grid(row=1, column=1, padx=10, pady=5, sticky='ew')

        ttk.Button(self.root, text="Agregar", command=self.validar_y_agregar).grid(row=2, column=0, columnspan=2, pady=10)

        self.root.columnconfigure(0, weight=1)
        self.root.columnconfigure(1, weight=1)
        self.root.protocol("WM_DELETE_WINDOW", self.cerrar_ventana)  # Vincular el cierre de la ventana

        self.root.mainloop()

    def validar_y_agregar(self):
        user_id = self.entry_user_id.get()
        access_token = self.entry_access_token.get()

        if not user_id or not access_token:
            messagebox.showerror("Error", "Ambas casillas deben estar completas.")
        else:
            self.user_id = user_id
            self.access_token = access_token
            datos_user = {
                'idUSER': self.user_id,
                'AUTH_TOKEN': self.access_token
            }            
            try:
                self.conexionDBA.insertar_datos_sin_obtener_id("MPQRCODE_CLIENTE", datos_user)
                self.root.destroy()
                print("DATOS AGREGADOS")
            except Exception as e:
                messagebox.showerror("Error", f"Error al insertar datos en la base de datos: {str(e)}")

    def cerrar_ventana(self):
        self.root.destroy()

class GUIconexiones:
    def __init__(self, conexionDBA):
        self.conexionDBA = conexionDBA
        self.id_user = self.conexionDBA.specify_search("MPQRCODE_CLIENTE", 'idUSER', 1)
        self.token  = self.conexionDBA.specify_search("MPQRCODE_CLIENTE", 'AUTH_TOKEN', 1)
        self.datos_connect = (self.id_user, self.token)
        self.ventana_principal = None 
        self.conexionAPI = Conexion_APP(self.datos_connect, self.conexionDBA)

    def crear_ventana_principal(self):
        self.ventana_principal = tk.Tk()
        self.ventana_principal.title("Menú Principal")

        boton_config = {'width': 20}
        estilo = ttk.Style()
        estilo.configure("TButton", font=('Helvetica', 10))

        ttk.Button(self.ventana_principal, text="Crear Sucursal", command=self.crear_sucursal_app, **boton_config).grid(row=0, column=0, pady=5, sticky='nsew')
        ttk.Button(self.ventana_principal, text="Crear Caja", command=self.crear_caja_app, **boton_config).grid(row=1, column=0, pady=5, sticky='nsew')
        ttk.Button(self.ventana_principal, text="Crear Orden", command=self.crear_orden_app, **boton_config).grid(row=2, column=0, pady=5, sticky='nsew')

        ttk.Button(self.ventana_principal, text="Eliminar Sucursal", command=self.mostrar_ventana_creacion_orden, **boton_config).grid(row=0, column=1, pady=5, padx=5, sticky='nsew')
        ttk.Button(self.ventana_principal, text="Configurar Caja", command=self.config_orden_app, **boton_config).grid(row=1, column=1, pady=5, padx=5, sticky='nsew')
        ttk.Button(self.ventana_principal, text="Eliminar Orden", command=self.mostrar_ventana_creacion_orden, **boton_config).grid(row=2, column=1, pady=5, padx=5, sticky='nsew')

        self.ventana_principal.columnconfigure(0, weight=1)
        self.ventana_principal.columnconfigure(1, weight=1)
        self.ventana_principal.rowconfigure([0, 1, 2], weight=1)

        self.ventana_principal.geometry("500x250")

        self.ventana_principal.mainloop()            

    def crear_sucursal_app(self):
        try:
            crear_sucursal_app_instance = CrearSucursalApp(self.conexionAPI)
            crear_sucursal_app_instance.create_widgets()
        except Exception as e:
            messagebox.showerror("Error", f"Error al crear la instancia de CrearSucursalApp: {str(e)}")

    def crear_caja_app(self):
        try:
            crear_caja_app_instance = CrearCajaApp(self.conexionAPI, self.conexionDBA)
        except Exception as e:
            print(f"Error: {e}")
            
    def crear_orden_app(self):
        try:
            crear_orden_app_instance = CrearOrdenApp(self.conexionAPI, self.conexionDBA)
        except Exception as e:
                print(f"Error: {e}")
                
    def config_orden_app(self):
        try:
            config_orden_app_instance = ConfigurarCajaApp(self.conexionAPI, self.conexionDBA)
        except Exception as e:
                print(f"Error: {e}")
    
    def mostrar_ventana_creacion_orden(self):
        # Código para la ventana de creación de orden
        pass
    
if __name__ == "__main__":
    config = ConfigInicialMPQRCODE()