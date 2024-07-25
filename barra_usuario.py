import tkinter as tk
from tkinter import ttk, messagebox
import mysql.connector

# Configuración de la conexión a la base de datos
DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': '',
    'database': 'molitorm'
}

def conectar_bd():
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        return conn
    except mysql.connector.Error as err:
        messagebox.showerror("Error de conexión", f"No se pudo conectar a la base de datos: {err}")
        return None

def fetch_data(query, params=None):
    conn = conectar_bd()
    if conn:
        try:
            cursor = conn.cursor()
            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)
            result = cursor.fetchall()
            cursor.close()
            conn.close()
            return result
        except mysql.connector.Error as err:
            messagebox.showerror("Error de consulta", f"Error al ejecutar la consulta: {err}")
    return []

def show_register_user(frame):
    for widget in frame.winfo_children():
        widget.destroy()

    frame.configure(bg="white")
    frame.grid_columnconfigure(0, weight=1)
    frame.grid_rowconfigure(1, weight=1)
    
    # Título fuera del frame
    title_label = tk.Label(frame, text="Registrar Usuario", font=("Helvetica", 16, "bold"), bg="white")
    title_label.grid(row=0, column=0, pady=(20, 10))

    center_frame = tk.Frame(frame, bg="white")
    center_frame.grid(row=1, column=0, sticky="nsew")
    center_frame.grid_columnconfigure(0, weight=1)
    center_frame.grid_rowconfigure(0, weight=1)

    form_frame = tk.Frame(center_frame, bg="#BDDB8C", relief="ridge", borderwidth=2)
    form_frame.grid(row=0, column=0, padx=20, pady=20)

    labels = ["Nombre:", "Apellido Paterno:", "Apellido Materno:", "Correo electrónico:", "Contraseña:", "Cargo de trabajo:"]
    entries = []

    for i, label in enumerate(labels):
        tk.Label(form_frame, text=label, bg="#BDDB8C").grid(row=i, column=0, padx=10, pady=5, sticky="e")
        if i < 5:  # Para todos excepto el último (Cargo de trabajo)
            entry = tk.Entry(form_frame, width=30)
            entry.grid(row=i, column=1, padx=10, pady=5, sticky="w")
            entries.append(entry)
        else:
            cargos = fetch_data("SELECT id_cargo, nombre FROM cargo")
            cargo_combobox = ttk.Combobox(form_frame, values=[f"{id_cargo} - {nombre}" for id_cargo, nombre in cargos], width=27)
            cargo_combobox.grid(row=i, column=1, padx=10, pady=5, sticky="w")
            entries.append(cargo_combobox)

    entries[4].config(show="*")  # Configurar la entrada de contraseña para mostrar asteriscos

    def registrar_usuario():
        valores = [entry.get() for entry in entries]
        cargo_seleccionado = valores[-1].split(" - ")[0] if valores[-1] else None

        if all(valores[:-1]) and cargo_seleccionado:  # Verificar que todos los campos estén llenos
            conn = conectar_bd()
            if conn:
                try:
                    cursor = conn.cursor()
                    query = """
                        INSERT INTO usuarios (nombre, a_paterno, a_materno, correo, contraseña, id_cargo)
                        VALUES (%s, %s, %s, %s, %s, %s)
                    """
                    cursor.execute(query, (*valores[:-1], cargo_seleccionado))
                    conn.commit()
                    messagebox.showinfo("Registro exitoso", "Usuario registrado correctamente")
                    
                    # Limpiar los campos después del registro exitoso
                    for entry in entries[:-1]:
                        entry.delete(0, tk.END)
                    entries[-1].set('')  # Limpiar el combobox
                    
                except mysql.connector.Error as err:
                    messagebox.showerror("Error de registro", f"Error: {err}")
                finally:
                    cursor.close()
                    conn.close()
        else:
            messagebox.showwarning("Campos incompletos", "Por favor, complete todos los campos.")

    button_frame = tk.Frame(form_frame, bg="#BDDB8C")
    button_frame.grid(row=6, column=0, columnspan=2, pady=10)

    registrar_button = tk.Button(button_frame, text="Registrar", command=registrar_usuario)
    registrar_button.grid(row=0, column=0, padx=5)

    return entries  # Devolver las entradas para poder acceder a ellas desde fuera
