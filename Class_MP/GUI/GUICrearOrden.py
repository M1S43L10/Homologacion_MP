import tkinter as tk
from tkinter import ttk, messagebox

class CrearOrdenApp:
    def __init__(self, conexionAPI, conexionDBA):
        self.ventana_creacion_caja = tk.Tk()
        self.ventana_creacion_caja.title("Creación de Orden")
        self.conexionAPI = conexionAPI
        self.conexionDBA = conexionDBA
        
        self.datos_para_orden = self.conexionDBA.specify_search_all_columns("MPQRCODE_CONEXIONPROGRAMAS", "idINCREMENT", 1)
        self.datos_caja = self.conexionDBA.specify_search_all_columns("MPQRCODE_CAJA", "idINCREMENT", 1)
        print(self.datos_para_orden)
        print(self.datos_caja)
        
        response = self.conexionAPI.crearOrdenFULL(self.datos_caja[3], self.datos_para_orden[1], self.datos_caja[1], self.datos_para_orden[3], self.datos_caja[4])
        if response == True:
            messagebox.showinfo("Exito", "Pago realizado")
            self.conexionAPI.eliminarOrdenesPostDBA()
        else:
            messagebox.showerror("Error", "No se recibio el pago")