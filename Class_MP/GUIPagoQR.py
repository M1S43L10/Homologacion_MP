import tkinter as tk
from tkinter import simpledialog
from PIL import  ImageTk
from qrcode.main import QRCode
from Conexion_APIs_MP import Conexion_Api

class InterfazMercadoPago(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("MercadoPago QR Generator")
        self.geometry("300x300")

        # Solicitar user_id y access_token al usuario
        self.user_id = str(simpledialog.askstring("Input", "Ingrese el User ID:"))
        self.access_token = str(simpledialog.askstring("Input", "Ingrese el Access Token:"))

        self.label_monto = tk.Label(self, text="Monto a Pagar:")
        self.entry_monto = tk.Entry(self)

        self.label_sucursal = tk.Label(self, text="Sucursal:")
        self.entry_sucursal = tk.Entry(self)

        self.label_caja = tk.Label(self, text="Nro de Caja:")
        self.entry_caja = tk.Entry(self)

        self.button_generar_qr = tk.Button(self, text="Generar QR", command=self.generar_qr)
        self.button_pagar = tk.Button(self, text="Pagar", command=self.pagar)

        self.label_monto.pack(pady=5)
        self.entry_monto.pack(pady=5)
        self.label_sucursal.pack(pady=5)
        self.entry_sucursal.pack(pady=5)
        self.label_caja.pack(pady=5)
        self.entry_caja.pack(pady=5)
        self.button_generar_qr.pack(pady=5)
        self.button_pagar.pack(pady=10)

        self.conexion_api = Conexion_Api(self.user_id, self.access_token)

    def generar_qr(self):
        monto = self.entry_monto.get()
        sucursal = self.entry_sucursal.get()
        caja = self.entry_caja.get()

        if monto and sucursal and caja:
            # Llamar a la función existente en la clase Conexion_Api
            response1 = self.conexion_api.crear_orden_dinamico(float(monto), str(sucursal), str(caja))
            # Simula la obtención del código QR (reemplaza esto con tu código real)
            json_data = response1.json()
            qr_data = json_data['qr_data']
            print(qr_data)

            # Crear el código QR con un tamaño más pequeño
            qr = QRCode(version=3, box_size=8.5, border=2)
            qr.add_data(str(qr_data))
            qr.make(fit=True)

            # Crear la imagen del código QR directamente
            img = qr.make_image(fill_color=(0, 0, 0), back_color=(255, 255, 255))

            # Crear una ventana Toplevel en lugar de una nueva instancia de Tk
            ventana = tk.Toplevel(self)
            ventana.title("Código QR")

            # Convertir la imagen del código QR a un objeto PhotoImage de Tkinter
            imagen_tk = ImageTk.PhotoImage(img)

            # Crear un widget Label para mostrar la imagen
            etiqueta = tk.Label(ventana, image=imagen_tk)
            etiqueta.pack(padx=5, pady=5)  # Ajusta el espacio alrededor de la imagen

            # Establecer el tamaño de la ventana
            ventana.geometry("400x400")  # Ajusta el tamaño de la ventana según tus necesidades

            # Ejecutar el bucle de eventos de Tkinter
            ventana.mainloop()

            
        else:
            tk.messagebox.showerror("Error", "Ingresa todos los valores")

    def pagar(self):
        # Puedes agregar aquí la lógica para procesar el pago si es necesario
        tk.messagebox.showinfo("Pagar", "¡Pago exitoso!")