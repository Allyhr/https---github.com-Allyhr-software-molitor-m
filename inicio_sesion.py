import tkinter as tk
from tkinter import messagebox
import mysql.connector
from PIL import Image, ImageTk
import os
import sys

def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

class InicioSesion(tk.Frame):
    def __init__(self, master, on_login_success):
        super().__init__(master)
        self.master = master
        self.on_login_success = on_login_success
        self.grid(sticky="nsew")
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.crear_widgets()

    def crear_widgets(self):
        # Cargar la imagen de fondo
        image_path = resource_path(os.path.join("images", "fondo1.jpg"))
        self.background_image = Image.open(image_path)

        # Crear un canvas para el fondo
        self.canvas = tk.Canvas(self)
        self.canvas.grid(row=0, column=0, sticky="nsew")

        # Crear la imagen de fondo
        self.canvas.create_image(0, 0, anchor="nw", tags="bg")

        # Título centrado
        self.title_id = self.canvas.create_text(400, 100, text="Iniciar Sesión", font=("Helvetica", 24, "bold"), fill="white")

        # Elementos de inicio de sesión
        self.email_label_id = self.canvas.create_text(300, 200, text="Correo electronico:", font=("Helvetica", 10), fill="white")
        self.email_var = tk.StringVar()
        self.email_entry = tk.Entry(self.canvas, textvariable=self.email_var)
        self.email_entry_id = self.canvas.create_window(450, 200, window=self.email_entry)

        self.password_label_id = self.canvas.create_text(300, 250, text="Contraseña:", font=("Helvetica", 10), fill="white")
        self.password_var = tk.StringVar()
        self.password_entry = tk.Entry(self.canvas, textvariable=self.password_var, show="*")
        self.password_entry_id = self.canvas.create_window(450, 250, window=self.password_entry)

        # Botón de inicio de sesión
        self.login_button = tk.Button(self.canvas, text="Iniciar Sesión", command=self.login, bg="white", fg="black")
        self.login_button_id = self.canvas.create_window(400, 300, window=self.login_button)

        # Vincular el evento de redimensionamiento
        self.bind("<Configure>", self.resize_background)

        # Llamar a resize_background inicialmente para configurar todo
        self.after(100, self.resize_background)  # Pequeño retraso para asegurar que el widget esté completamente creado

    def resize_background(self, event=None):
        new_width = self.winfo_width()
        new_height = self.winfo_height()
        resized_image = self.background_image.resize((new_width, new_height), Image.Resampling.LANCZOS)
        new_photo = ImageTk.PhotoImage(resized_image)
        self.canvas.delete("bg")
        self.canvas.create_image(0, 0, image=new_photo, anchor="nw", tags="bg")
        self.canvas.image = new_photo  # Mantener una referencia

        # Asegurar que la imagen de fondo esté detrás de todo
        self.canvas.tag_lower("bg")

        # Reposicionar elementos
        center_x = new_width // 2
        self.canvas.coords(self.title_id, center_x, 100)
        self.canvas.coords(self.email_label_id, center_x - 100, 200)
        self.canvas.coords(self.email_entry_id, center_x + 50, 200)
        self.canvas.coords(self.password_label_id, center_x - 100, 250)
        self.canvas.coords(self.password_entry_id, center_x + 50, 250)
        self.canvas.coords(self.login_button_id, center_x, 300)

    def login(self):
        usuario = self.email_var.get()
        password = self.password_var.get()

        try:
            conexion = mysql.connector.connect(
                host="localhost",
                user="root",
                password="",
                database="molitorm"
            )

            cursor = conexion.cursor()
            query = "SELECT * FROM usuarios WHERE correo = %s AND contraseña = %s"
            cursor.execute(query, (usuario, password))
            resultado = cursor.fetchone()

            if resultado:
                messagebox.showinfo("Éxito", "Inicio de sesión exitoso")
                self.on_login_success()
            else:
                messagebox.showerror("Error", "Usuario o contraseña incorrectos")

            cursor.close()
            conexion.close()

        except mysql.connector.Error as error:
            messagebox.showerror("Error de Base de Datos", str(error))