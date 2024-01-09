import tkinter as tk
from tkinter import ttk, Button
from ttkthemes import ThemedStyle
import ast
from tkinter import Label, Entry, messagebox, Toplevel

class InterfazDatos:
    def __init__(self):
        self.entry_clave = None
        self.entry_nombre = None
        self.entry_edad = None
        self.clave_seleccionada = None

        self.ventana = tk.Tk()
        self.ventana.title("Interfaz para Guardar Datos")

        # Aplicar el tema "clearlooks" al estilo ttk
        style = ThemedStyle(self.ventana)
        style.set_theme("clearlooks")

        Label(self.ventana, text="Sucursal Central:").grid(row=0, column=0, padx=10, pady=10)
        Label(self.ventana, text="USER ID:").grid(row=1, column=0, padx=10, pady=10)
        Label(self.ventana, text="ACCESS TOKEN:").grid(row=2, column=0, padx=10, pady=10)

        # Utilizar ttk.Entry en lugar de Entry para casillas modernas
        self.entry_clave = ttk.Entry(self.ventana)
        self.entry_nombre = ttk.Entry(self.ventana)
        self.entry_edad = ttk.Entry(self.ventana)

        self.entry_clave.grid(row=0, column=1, padx=10, pady=10)
        self.entry_nombre.grid(row=1, column=1, padx=10, pady=10)
        self.entry_edad.grid(row=2, column=1, padx=10, pady=10)

        # Utilizar ttk.Button en lugar de Button para botones modernos
        self.boton_guardar = ttk.Button(self.ventana, text="Guardar Datos", command=self.guardar_datos)
        self.boton_guardar.grid(row=3, column=0, columnspan=2, pady=10)

        self.boton_mostrar = ttk.Button(self.ventana, text="Mostrar Valores", command=self.mostrar_valores)
        self.boton_mostrar.grid(row=4, column=0, columnspan=2, pady=10)

    def cargar_diccionario(self):
        try:
            with open('datos_guardados.py', 'r') as archivo:
                contenido = archivo.read()
                diccionario = ast.literal_eval(contenido)
            return diccionario
        except FileNotFoundError:
            return {}

    def guardar_diccionario(self, diccionario):
        with open('datos_guardados.py', 'w') as archivo:
            archivo.write(repr(diccionario))

    def agregar_datos(self, diccionario, clave, valor):
        diccionario[clave] = valor

    def eliminar_valor(self, diccionario, clave):
        if clave in diccionario:
            del diccionario[clave]
            self.guardar_diccionario(diccionario)  # Agregar esta línea para guardar después de eliminar

    def guardar_datos(self):
        clave = str(self.entry_clave.get())
        ID_ACCOUNT = str(self.entry_nombre.get())
        ACCESS_TOKEN = str(self.entry_edad.get())

        mi_diccionario = self.cargar_diccionario()

        if clave not in mi_diccionario:
            mi_diccionario[clave] = {}

        self.agregar_datos(mi_diccionario[clave], 'ID_ACCOUNT', ID_ACCOUNT)
        self.agregar_datos(mi_diccionario[clave], 'ACCESS_TOKEN', ACCESS_TOKEN)

        self.guardar_diccionario(mi_diccionario)
        messagebox.showinfo("Éxito", "Datos guardados correctamente.")

        # Limpiar las casillas después de guardar
        self.entry_clave.delete(0, tk.END)
        self.entry_nombre.delete(0, tk.END)
        self.entry_edad.delete(0, tk.END)

    def mostrar_valores(self):
        mi_diccionario = self.cargar_diccionario()

        if not mi_diccionario:
            messagebox.showinfo("Info", "No hay valores guardados.")
            return

        ventana_mostrar = Toplevel(self.ventana)
        ventana_mostrar.title("Valores Guardados")

        # Crear un Treeview para mostrar los valores en una tabla
        tree = ttk.Treeview(ventana_mostrar, columns=('Sucursal', 'ID', 'TOKEN'), show='headings')
        tree.heading('Sucursal', text='Sucursal')
        tree.heading('ID', text='ID')
        tree.heading('TOKEN', text='TOKEN')

        for clave, valores in mi_diccionario.items():
            id_account = valores.get('ID_ACCOUNT', 'N/A')
            access_token = valores.get('ACCESS_TOKEN', 'N/A')
            tree.insert('', 'end', values=(clave, id_account, access_token), tags=(clave,))

        tree.pack(expand=tk.YES, fill=tk.BOTH)

        def seleccionar_clave(event):
            seleccion = tree.selection()
            if seleccion:
                item = seleccion[0]
                self.clave_seleccionada = tree.item(item, 'tags')[0]
            else:
                # Aquí puedes manejar el caso en el que no hay elementos seleccionados
                # Por ejemplo, puedes mostrar un mensaje o realizar otra acción.
                print("Ningún elemento seleccionado")


        def eliminar_seleccion():
            ventana_mostrar.destroy()  # Cerrar la ventana actual
            self.eliminar_valor(mi_diccionario, self.clave_seleccionada)
            self.mostrar_valores()  # Abrir la nueva ventana actualizada
            messagebox.showinfo("Éxito", "Valor eliminado de manera exitosa.")

        boton_eliminar = Button(ventana_mostrar, text="Eliminar", command=eliminar_seleccion)
        boton_eliminar.pack(pady=10)

        # Iniciar el bucle principal de la ventana de verificación de contraseña
        ventana_mostrar.mainloop()

if __name__ == "__main__":
    # Crear una instancia de la clase InterfazDatos
    interfaz = InterfazDatos()

    # Iniciar el bucle principal de la ventana
    interfaz.ventana.mainloop()