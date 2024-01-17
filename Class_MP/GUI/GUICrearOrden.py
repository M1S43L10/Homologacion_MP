import tkinter as tk
from tkinter import ttk, messagebox
import customtkinter
import threading
import time

class CrearOrdenApp:
    def __init__(self, conexionAPI, conexionDBA):
        customtkinter.set_appearance_mode("white")
        customtkinter.set_default_color_theme("blue")
        self.ventana_creacion_caja = customtkinter.CTk()
        self.ventana_creacion_caja.title("Creación de Orden")
        self.ventana_creacion_caja.geometry("500x250")
        self.conexionAPI = conexionAPI
        self.conexionDBA = conexionDBA        

        self.datos_para_orden = self.conexionDBA.specify_search_all_columns("MPQRCODE_CONEXIONPROGRAMAS", "idINCREMENT", 1)
        self.datos_caja = self.conexionDBA.specify_search_all_columns("MPQRCODE_CAJA", "idINCREMENT", 1)
        print(self.datos_para_orden)
        print(self.datos_caja)
        
        self.id_order_var = tk.StringVar()
        self.step_one = None
        self.obtenerPago = None
        self.progresoNRO = 0
        
        self.my_progressbar = customtkinter.CTkProgressBar(self.ventana_creacion_caja, orientation="horizontal", determinate_speed=0.5)
        self.my_progressbar.pack(pady=40)    
        
        self.my_progressbar.set(0)
        
        my_button = customtkinter.CTkButton(self.ventana_creacion_caja, text="Crear Orden", command=self.functionMAIN)
        my_button.pack(pady=10)
        
        self.my_label_aviso = customtkinter.CTkLabel(self.ventana_creacion_caja, text="", font=("Helvetica", 18))
        self.my_label_aviso.pack(pady=10)
        
        self.my_label = customtkinter.CTkLabel(self.ventana_creacion_caja, text="", font=("Helvetica", 18))
        self.my_label.pack(pady=10)
        
        self.ventana_creacion_caja.mainloop()    

    def update_window(self):
        self.ventana_creacion_caja.update_idletasks()

    def clicker(self):
        self.my_progressbar.step()
        self.my_label.configure(text=str((int(self.my_progressbar.get()*100))) + "%")
        """self.progresoNRO = int(self.my_progressbar.get()*100)
        print(self.progresoNRO)"""        
        self.update_window()
        
        
    def functionMAIN(self):
        self.crear_orden()
        threading.Thread(target=self.clickerFull).start()
        
    def clickerFull(self):
        clickerProgress = int(self.my_progressbar.get()*100)
        while not clickerProgress == 99:
            if clickerProgress <= 25:
                self.my_label_aviso.configure(text="Creando Orden...")
                if not clickerProgress == 25:
                    while not clickerProgress == 25:
                        self.clicker()
                        clickerProgress = int(self.my_progressbar.get()*100)
                        print(clickerProgress)
                        time.sleep(0.05)
                    else:
                        self.clicker()
                        clickerProgress = int(self.my_progressbar.get()*100)
                        print(clickerProgress)
                        time.sleep(0.5)
                        self.my_label_aviso.configure(text="Orden Creada. Escanee el QR")
            elif clickerProgress < 50:
                if not clickerProgress == 50:
                    while not clickerProgress == 50 and type(self.id_order_var.get()) == str:
                        self.clicker()
                        clickerProgress = int(self.my_progressbar.get()*100)
                        print(clickerProgress)
                        time.sleep(0.25)
                    else:
                        clickerProgress = int(self.my_progressbar.get()*100)
                        print(clickerProgress)
                        time.sleep(0.25)
                        self.my_label_aviso.configure(text="Esperando Pago...")
                        self.obtneridOrden(self.step_one)
                        self.clicker()
            elif clickerProgress < 80:
                self.obtenerPago = self.obtnerPago(self.step_one, self.id_order_var.get())
                if not clickerProgress == 80:
                    while not clickerProgress == 80:
                        if self.id_order_var.get() == "":
                            self.clicker()
                            clickerProgress = int(self.my_progressbar.get()*100)
                            print(clickerProgress)
                        else:
                            self.clicker()
                            clickerProgress = int(self.my_progressbar.get()*100)
                            print(clickerProgress)
                    else:
                        self.clicker()
                        clickerProgress = int(self.my_progressbar.get()*100)
                        print(clickerProgress)
                        time.sleep(0.05)
                        self.my_label_aviso.configure(text="Comparando Registros...")                        
            elif clickerProgress < 100:
                if not clickerProgress == 99:
                    while not clickerProgress == 99:
                        self.clicker()
                        clickerProgress = int(self.my_progressbar.get()*100)
                        print(clickerProgress)
                        time.sleep(0.05)
                    else:
                        self.my_progressbar.set(100)
                        self.my_label_aviso.configure(text="Pago Recibido")
            time.sleep(0.05)
        self.finalizarPago(self.obtenerPago)     
    """
    def progreso(self, nro_progreso, respuesta):
        status_progreso = nro_progreso
        print(status_progreso)        
        self.my_progressbar.set(nro_progreso)
        self.update_window()
        if self.progresoNRO < 26:
            print("a")
            self.my_label_aviso.configure(text="Creando Orden...")
            self.clicker()
        elif self.progresoNRO < 51:
            print("b")
            self.my_label_aviso.configure(text="Orden Creada. Escanee el QR")
            self.clicker()
        elif self.progresoNRO < 81:
            print("c")
            self.my_label_aviso.configure(text="Esperando Pago...")
            self.clicker()
        else:
            print("z")
            self.my_label_aviso.configure(text="Pago Realizado")
            self.clicker()
            self.finalizarPago(respuesta)
            
        self.my_progressbar.start()
        print(status_progreso)
        
    def realizar_orden(self):        
        orden = self.crear_orden()
        self.obtneridOrder(orden)
        obtenerPago = self.obtnerPago(orden, self.id_order_var.get())
        """
        
    def crear_orden(self):
        self.step_one = self.conexionAPI.crearOrden(self.datos_caja[3], self.datos_para_orden[1], self.datos_caja[1], self.datos_para_orden[3], self.datos_caja[4])
        print(f"step_one: {self.step_one}")
    
    def obtneridOrden(self, step_one):
        step_two = self.conexionAPI.obteneridOrder(step_one[0], step_one[1])
        self.id_order_var.set(step_two[0])
        print(f"step_two {self.id_order_var.get()}")
    
    def obtnerPago(self, step_one, step_two):
        print(f"step_two {self.id_order_var.get()}")
        response = self.conexionAPI.obtenerPago(step_two, step_one[0], step_one[1])
        return response
        
    def finalizarPago(self, respuesta):
        response = respuesta
        if response == True:
            messagebox.showinfo("Exito", "Pago Recibido")
            self.conexionAPI.eliminarOrdenesPostDBA()
            self.ventana_creacion_caja.destroy()
        else:
            messagebox.showerror("Error", "No se recibió el pago")
