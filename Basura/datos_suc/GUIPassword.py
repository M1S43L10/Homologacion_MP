import tkinter as tk
from tkinter import Entry, Button, Label, messagebox
from interfaz_datos import InterfazDatos  # Importar la clase InterfazDatos desde el archivo interfaz_datos.py

class VentanaContraseña:
    def __init__(self):
        self.ventana_contrasena = tk.Tk()
        self.ventana_contrasena.title("Verificación de Contraseña")

        Label(self.ventana_contrasena, text="Contraseña:").pack(pady=10)

        self.entry_contrasena = Entry(self.ventana_contrasena, show="*")
        self.entry_contrasena.pack(pady=10)

        boton_verificar = Button(self.ventana_contrasena, text="Verificar", command=self.verificar_contrasena)
        boton_verificar.pack(pady=10)

    def verificar_contrasena(self):
        contrasena_ingresada = self.entry_contrasena.get()
        if contrasena_ingresada == "***":  # Reemplaza "***" con tu contraseña real
            self.ventana_contrasena.destroy()  # Cerrar la ventana de verificación de contraseña
            InterfazDatos()  # Instanciar la clase InterfazDatos
        else:
            messagebox.showerror("Error", "Contraseña incorrecta")

if __name__ == "__main__":
    # Crear una instancia de la clase VentanaContraseña
    ventana_contrasena = VentanaContraseña()

    # Iniciar el bucle principal de la ventana de verificación de contraseña
    ventana_contrasena.ventana_contrasena.mainloop()
