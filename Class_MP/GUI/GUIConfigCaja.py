import tkinter as tk
from tkinter import ttk, messagebox

class ConfigurarCajaApp:
    def __init__(self, conexionAPI, conexionDBA):
        self.conexionAPI = conexionAPI
        self.conexionDBA = conexionDBA
        if self.tabla_caja_vacia():
            self.ventana_config_caja = tk.Tk()
            self.ventana_config_caja.title("Configurar Caja")
            
            # Agregar ComboBox para elegir la sucursal
            self.label_Caja = ttk.Label(self.ventana_config_caja, text="Seleccione con que Caja va a trabajar:")
            self.label_Caja.grid(row=0, column=0, padx=10, pady=5, sticky='w')
            self.selected_name = tk.StringVar()
            
            # Obtener todos los External IDs de la tabla MPQRCODE_CAJAS
            self.name = self.obtener_todos_los_name('MPQRCODE_CAJAS')

            # ComboBox con los resultados de la función
            self.combo_CAJAS = ttk.Combobox(self.ventana_config_caja, values=self.name, textvariable=self.selected_name)
            self.combo_CAJAS.grid(row=0, column=1, padx=10, pady=5, sticky='ew')
            
            # Botón para cargar la config del POS
            ttk.Button(self.ventana_config_caja, text="Agregar", command=self.guardar_config).grid(row=1, column=0, columnspan=2, pady=10)      
        else:
            messagebox.showinfo("Existente", "Ya existe una Caja cargada en el sistema")
        
    def tabla_caja_vacia(self):
        try:
            return self.conexionDBA.contar_registros("MPQRCODE_CAJA") == 0
        except Exception as e:
            messagebox.showerror("Error", f"Error al contar registros: {str(e)}")
            
    def obtener_todos_los_name(self, tabla):
        try:
            # Implementa la lógica para obtener los External IDs desde la base de datos
            # Puedes usar tu función existente
            name = self.conexionDBA.obtener_todos_los_name(tabla)
            return name
        except Exception as e:
            messagebox.showerror("Error", f"Error al obtener los External IDs: {e}")
            
    def guardar_config(self):
        try:
            print(self.combo_CAJAS.get())
            datosObtnerCajas = ['external_store_id', "external_id", "picture_url"]
            datosObtenidosCajas = []
            for columna in datosObtnerCajas:
                datosObtenidosCajas.append(self.conexionDBA.specify_search_condicion("MPQRCODE_CAJAS", columna, "name", self.combo_CAJAS.get()))
            print(datosObtenidosCajas)
            print(self.conexionDBA.specify_search_condicion("MPQRCODE_SUCURSAL", 'name', 'external_id', datosObtenidosCajas[0]))
            datosObtenidosCajasDICT = {
                "sucNAME": self.conexionDBA.specify_search_condicion("MPQRCODE_SUCURSAL", 'name', 'external_id', datosObtenidosCajas[0]),
                "posNAME": self.combo_CAJAS.get(),
                "external_id_pos": datosObtenidosCajas[1],
                "pictureURL": datosObtenidosCajas[2]
            }
            print(datosObtenidosCajasDICT)
            self.conexionDBA.insertar_datos_sin_obtener_id("MPQRCODE_CAJA", datosObtenidosCajasDICT)
            datosObtnerSuc = datosObtenidosCajas[0]
        except Exception as e:
            print(e)
            messagebox.showerror("Error", f"Error al configurar la Caja: {e}")
        finally:
                self.ventana_config_caja.destroy()      