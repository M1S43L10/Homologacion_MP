import tkinter as tk
from tkinter import messagebox
from Class_MP.database import ConexionMySQL

class InterfazLogin:
    def __init__(self, root):
        self.root = root
        self.root.title("Login")
        
        # Variables para almacenar usuario y contraseña
        self.usuario_var = tk.StringVar()
        self.contrasena_var = tk.StringVar()
        
        # Etiquetas y campos de entrada
        tk.Label(root, text="Usuario:").grid(row=0, column=0, padx=10, pady=10)
        tk.Entry(root, textvariable=self.usuario_var).grid(row=0, column=1, padx=10, pady=10)
        
        tk.Label(root, text="Contraseña:").grid(row=1, column=0, padx=10, pady=10)
        tk.Entry(root, textvariable=self.contrasena_var, show="*").grid(row=1, column=1, padx=10, pady=10)
        
        # Botón de inicio de sesión
        tk.Button(root, text="Iniciar Sesión", command=self.iniciar_sesion).grid(row=2, column=0, columnspan=2, pady=10)

    def iniciar_sesion(self):
        usuario = str(self.usuario_var.get())
        contrasena = str(self.contrasena_var.get())

        acceso_bd = {
            "host": "localhost",
            "user": usuario,
            "password": contrasena,
            "database": "datos_mercadopago"
        }

        # Intentar la conexión a la base de datos
        conexion_mysql = ConexionMySQL(**acceso_bd)

        if conexion_mysql.conectar():
            messagebox.showinfo("Éxito", "Conexión a MySQL establecida exitosamente.")
            self.root.destroy()  # Cerrar la ventana después de una conexión exitosa
        else:
            messagebox.showerror("Error", "Usuario o contraseña incorrectos. Intente nuevamente.")

# Crear la ventana principal
root = tk.Tk()
app = InterfazLogin(root)
root.mainloop()
