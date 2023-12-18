import tkinter as tk
from tkinter import simpledialog, messagebox
from PIL import ImageTk
from qrcode.main import QRCode
from Conexion_APIs_MP import Conexion_Api
import json

class InterfazMercadoPago(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("MercadoPago QR Generator")
        self.geometry("300x300")

        # Cargar datos desde el archivo datos_guardados.py
        self.datos_sucursal = self.cargar_datos_sucursal()

        # Obtener user_id y access_token desde el diccionario
        self.user_id = self.datos_sucursal.get('ID_ACCOUNT', '')
        self.access_token = self.datos_sucursal.get('ACCESS_TOKEN', '')

        self.label_monto = tk.Label(self, text="Monto a Pagar:")
        self.entry_monto = tk.Entry(self)

        # Obtener la sucursal del archivo Anonimo.json
        self.sucursal = self.obtener_sucursal()
        self.label_sucursal = tk.Label(self, text="Sucursal:", textvariable=self.sucursal)

        self.label_caja = tk.Label(self, text="Nro de Caja:")
        self.entry_caja = tk.Entry(self)

        self.button_generar_qr = tk.Button(self, text="Generar QR", command=self.generar_qr)
        self.button_pagar = tk.Button(self, text="Pagar", command=self.pagar)

        self.label_monto.pack(pady=5)
        self.entry_monto.pack(pady=5)
        self.label_sucursal.pack(pady=5)
        self.label_caja.pack(pady=5)
        self.entry_caja.pack(pady=5)
        self.button_generar_qr.pack(pady=5)
        self.button_pagar.pack(pady=10)

        self.conexion_api = Conexion_Api(self.user_id, self.access_token)

    def cargar_datos_sucursal(self):
        try:
            with open('datos_suc/datos_guardados.py', 'r') as archivo:
                contenido = archivo.read()
                diccionario = eval(contenido)  # No recomendado, pero aquí se usa por simplicidad
            return diccionario.get('TEST', {})
        except FileNotFoundError:
            return {}

    def obtener_sucursal(self):
        try:
            with open('SUCURSALES.JSON/Anonimo.json', 'r') as archivo:
                contenido = json.load(archivo)
                return contenido.get('name', 'N/A')
        except FileNotFoundError:
            return 'N/A'

    def generar_qr(self):
        monto = self.entry_monto.get()
        caja = self.entry_caja.get()

        if monto and caja:
            response1 = self.conexion_api.crear_orden_dinamico(float(monto), str(self.sucursal), str(caja))
            json_data = response1.json()
            qr_data = json_data['qr_data']

            qr = QRCode(version=3, box_size=8.5, border=2)
            qr.add_data(str(qr_data))
            qr.make(fit=True)

            img = qr.make_image(fill_color=(0, 0, 0), back_color=(255, 255, 255))

            ventana = tk.Toplevel(self)
            ventana.title("Código QR")

            imagen_tk = ImageTk.PhotoImage(img)

            etiqueta = tk.Label(ventana, image=imagen_tk)
            etiqueta.pack(padx=5, pady=5)

            ventana.geometry("400x400")
            ventana.mainloop()
        else:
            messagebox.showerror("Error", "Ingresa todos los valores")

    def pagar(self):
        messagebox.showinfo("Pagar", "¡Pago exitoso!")

if __name__ == "__main__":
    app = InterfazMercadoPago()
    app.mainloop()