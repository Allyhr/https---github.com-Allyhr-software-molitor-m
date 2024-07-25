import mysql.connector
from tkinter import messagebox, Toplevel, ttk, Label, LabelFrame
from tkcalendar import DateEntry
import tkinter as tk
from tkinter import ttk
import datetime

class DateEntry(ttk.Frame):
    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        
        self.year_var = tk.StringVar()
        self.month_var = tk.StringVar()
        self.day_var = tk.StringVar()
        
        current_date = datetime.date.today()
        
        self.year_entry = ttk.Spinbox(self, from_=1900, to=2100, width=4, textvariable=self.year_var)
        self.month_entry = ttk.Spinbox(self, from_=1, to=12, width=2, textvariable=self.month_var)
        self.day_entry = ttk.Spinbox(self, from_=1, to=31, width=2, textvariable=self.day_var)
        
        self.year_entry.pack(side=tk.LEFT)
        ttk.Label(self, text="-").pack(side=tk.LEFT)
        self.month_entry.pack(side=tk.LEFT)
        ttk.Label(self, text="-").pack(side=tk.LEFT)
        self.day_entry.pack(side=tk.LEFT)
        
        self.year_var.set(current_date.year)
        self.month_var.set(f"{current_date.month:02d}")
        self.day_var.set(f"{current_date.day:02d}")
    
    def get(self):
        return f"{self.year_var.get()}-{self.month_var.get().zfill(2)}-{self.day_var.get().zfill(2)}"

def conectar_bd():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="molitorm"
    )

def fetch_data(query):
    conn = conectar_bd()
    cursor = conn.cursor()
    cursor.execute(query)
    result = cursor.fetchall()
    conn.close()
    return result

def registrar_unidad(datos, register_window):
    try:
        conn = conectar_bd()
        cursor = conn.cursor()

        # Insertar en la tabla unidad
        query_unidad = """
        INSERT INTO unidad (matricula, fecha, id_fase, e_fechaInicio, e_semana, d_ancho, d_largo, d_alto, biomasa, id_alimentoh, 
        peso_alimentoh, id_sustrato, peso_sustrato, id_anaquel, id_estante, id_cuarto, id_tecnica, c_temperatura, c_humedad, c_oxigenacion) 
        VALUES (%(matricula)s, %(fecha)s, %(id_fase)s, %(e_fechaInicio)s, %(e_semana)s, %(d_ancho)s, %(d_largo)s, %(d_alto)s, 
        %(biomasa)s, %(id_alimentoh)s, %(peso_alimentoh)s, %(id_sustrato)s, %(peso_sustrato)s, %(id_anaquel)s, %(id_estante)s, 
        %(id_cuarto)s, %(id_tecnica)s, %(c_temperatura)s, %(c_humedad)s, %(c_oxigenacion)s)
        """
        cursor.execute(query_unidad, datos)

        # Obtener el ID de la unidad recién insertada
        id_unidad = cursor.lastrowid

        # Insertar en la tabla seguimiento_alimentacion
        query_seguimiento_alimentacion = """
        INSERT INTO seguimiento_alimentacion (id_unidad, ultima_alimentacion, proxima_alimentacion)
        VALUES (%s, NOW(), DATE_ADD(NOW(), INTERVAL 1 MINUTE))
        """
        cursor.execute(query_seguimiento_alimentacion, (id_unidad,))

        # Insertar en la tabla seguimiento_limpieza
        query_seguimiento_limpieza = """
        INSERT INTO seguimiento_limpieza (id_unidad, ultima_limpieza, proxima_limpieza)
        VALUES (%s, NOW(), DATE_ADD(NOW(), INTERVAL 1 MINUTE))
        """
        cursor.execute(query_seguimiento_limpieza, (id_unidad,))

        conn.commit()
        conn.close()
        messagebox.showinfo("Éxito", "Unidad registrada exitosamente")
        register_window.destroy()
    except mysql.connector.Error as err:
        messagebox.showerror("Error", f"Error: {err}")

def show_register_unit(root):
    def calcular_volumen():
        try:
            ancho = float(d_ancho_entry.get())
            largo = float(d_largo_entry.get())
            alto = float(d_alto_entry.get())
            volumen = ancho * largo * alto
            volumen_var.set(f"{volumen:.2f}")
        except ValueError:
            volumen_var.set("Error en las dimensiones")

    def calcular_densidad():
        try:
            volumen = float(volumen_var.get())
            biomasa = float(biomasa_entry.get())
            densidad = volumen / biomasa
            densidad_var.set(f"{densidad:.2f}")
        except ValueError:
            densidad_var.set("Error en volumen o biomasa")

    def on_registrar():
        datos = {
            "matricula": matricula_entry.get(),
            "fecha": fecha_entry.get(),
            "id_fase": fase_combobox.get().split(" - ")[0],
            "e_fechaInicio": e_fechaInicio_entry.get(),
            "e_semana": e_semana_combobox.get(),
            "d_ancho": d_ancho_entry.get(),
            "d_largo": d_largo_entry.get(),
            "d_alto": d_alto_entry.get(),
            "biomasa": biomasa_entry.get(),
            "id_alimentoh": alimentoh_combobox.get().split(" - ")[0],
            "peso_alimentoh": peso_alimentoh_entry.get(),
            "id_sustrato": sustrato_combobox.get().split(" - ")[0],
            "peso_sustrato": peso_sustrato_entry.get(),
            "id_anaquel": anaquel_combobox.get().split(" - ")[0],
            "id_estante": estante_combobox.get().split(" - ")[0],
            "id_cuarto": cuarto_combobox.get().split(" - ")[0],
            "id_tecnica": tecnica_combobox.get().split(" - ")[0],
            "c_temperatura": c_temperatura_entry.get(),
            "c_humedad": c_humedad_entry.get(),
            "c_oxigenacion": c_oxigenacion_entry.get(),
        }
        registrar_unidad(datos, register_window)

    register_window = Toplevel(root)
    register_window.title("Registrar Unidad")

    # Título
    Label(register_window, text="Registro de unidad de cria", fg="black", font=("Comic Sans", 17, "bold"),
          pady=10).pack()

    # Marco
    marco = LabelFrame(register_window, text="Informacion", font=("Comic Sans", 10, "bold"), pady=5)
    marco.config(bd=2)
    marco.pack(padx=10, pady=10)

    # INICIO FILA 0
    tk.Label(marco, text="ID unidad de cria:").grid(row=0, column=0, padx=10, pady=5, sticky="e")
    matricula_entry = tk.Entry(marco)
    matricula_entry.grid(row=0, column=1, padx=10, pady=5)

    tk.Label(marco, text="Fecha de alta de unidad de cria:").grid(row=0, column=4, padx=10, pady=5, sticky="e")
    fecha_entry = DateEntry(marco, width=12)
    fecha_entry.grid(row=0, column=5, padx=10, pady=5)

    # Espacio FILA 1
    tk.Label(marco, text="").grid(row=1, column=0, padx=10, pady=5)

    # ESTADIO FILA 2
    tk.Label(marco, text="Estadio:").grid(row=2, column=0, padx=10, pady=5, sticky="e")
    fases = fetch_data("SELECT id_fase, nombre FROM fase")
    fase_combobox = ttk.Combobox(marco, values=[f"{id_} - {nombre}" for id_, nombre in fases])
    fase_combobox.grid(row=2, column=1, padx=10, pady=5)

    tk.Label(marco, text="Fecha de estadio:").grid(row=2, column=2, padx=10, pady=10, sticky="e")
    e_fechaInicio_entry = DateEntry(marco, width=12)
    e_fechaInicio_entry.grid(row=2, column=3, padx=10, pady=5)

    tk.Label(marco, text="Semana(s):").grid(row=2, column=4, padx=10, pady=5, sticky="e")
    semanas = [str(i) for i in range(17)]
    e_semana_combobox = ttk.Combobox(marco, values=semanas)
    e_semana_combobox.grid(row=2, column=5, padx=10, pady=10)

    # Espacio FILA 3
    tk.Label(marco, text="Dimensiones de la unidad de cria").grid(row=3, column=0, padx=10, pady=5)

    # DIMENSIONES FILA 4
    tk.Label(marco, text="Ancho:").grid(row=4, column=0, padx=(2, 2), pady=5, sticky="e")
    d_ancho_entry = tk.Entry(marco)
    d_ancho_entry.grid(row=4, column=1, padx=(2, 2), pady=5)
    tk.Label(marco, text="cm").grid(row=4, column=2, padx=(2, 2), pady=5, sticky="w")

    tk.Label(marco, text="Largo:").grid(row=4, column=2, padx=(2, 2), pady=5, sticky="e")
    d_largo_entry = tk.Entry(marco)
    d_largo_entry.grid(row=4, column=3, padx=(2, 2), pady=5)
    tk.Label(marco, text="cm").grid(row=4, column=4, padx=(2, 2), pady=5, sticky="w")

    tk.Label(marco, text="Alto:").grid(row=4, column=4, padx=(2, 2), pady=5, sticky="e")
    d_alto_entry = tk.Entry(marco)
    d_alto_entry.grid(row=4, column=5, padx=(2, 2), pady=5)
    tk.Label(marco, text="cm").grid(row=4, column=6, padx=(2, 2), pady=5, sticky="w")

    # Espacio FILA 5
    tk.Label(marco, text="").grid(row=5, column=0, padx=10, pady=5)

    # VOLUMEN FILA 6
    volumen_var = tk.StringVar()
    tk.Label(marco, text="Volumen:").grid(row=6, column=0, padx=10, pady=5, sticky="e")
    volumen_label = tk.Label(marco, textvariable=volumen_var)
    volumen_label.grid(row=6, column=1, padx=10, pady=5)
    tk.Button(marco, text="Calcular Volumen", command=calcular_volumen).grid(row=6, column=2, padx=10, pady=5)

    # BIOMASA FILA 7
    tk.Label(marco, text="Biomasa:").grid(row=7, column=0, padx=10, pady=5, sticky="e")
    biomasa_entry = tk.Entry(marco)
    biomasa_entry.grid(row=7, column=1, padx=10, pady=5)

    # DENSIDAD FILA 8
    densidad_var = tk.StringVar()
    tk.Label(marco, text="Densidad:").grid(row=8, column=0, padx=10, pady=5, sticky="e")
    densidad_label = tk.Label(marco, textvariable=densidad_var)
    densidad_label.grid(row=8, column=1, padx=10, pady=5)
    tk.Button(marco, text="Calcular Densidad", command=calcular_densidad).grid(row=8, column=2, padx=10, pady=5)

    # Espacio FILA 9
    tk.Label(marco, text="").grid(row=9, column=0, padx=10, pady=5)

    # ALIMENTO HUMEDO FILA 10
    tk.Label(marco, text="Alimento humedo:").grid(row=10, column=0, padx=10, pady=5, sticky="e")
    alimentoh = fetch_data("SELECT id_alimentoh, nombre FROM alimentoh")
    alimentoh_combobox = ttk.Combobox(marco, values=[f"{id_} - {nombre}" for id_, nombre in alimentoh])
    alimentoh_combobox.grid(row=10, column=1, padx=10, pady=5)

    tk.Label(marco, text="Peso del alimento:").grid(row=10, column=2, padx=10, pady=5, sticky="e")
    peso_alimentoh_entry = tk.Entry(marco)
    peso_alimentoh_entry.grid(row=10, column=3, padx=10, pady=5)
    tk.Label(marco, text="Kg").grid(row=10, column=4, padx=(2, 2), pady=5, sticky="w")

    # SUSTRATO FILA 11
    tk.Label(marco, text="Sustrato:").grid(row=11, column=0, padx=10, pady=5, sticky="e")
    sustratos = fetch_data("SELECT id_sustrato, nombre FROM sustrato")
    sustrato_combobox = ttk.Combobox(marco, values=[f"{id_} - {nombre}" for id_, nombre in sustratos])
    sustrato_combobox.grid(row=11, column=1, padx=10, pady=5)

    tk.Label(marco, text="Peso del sustrato:").grid(row=11, column=2, padx=10, pady=5, sticky="e")
    peso_sustrato_entry = tk.Entry(marco)
    peso_sustrato_entry.grid(row=11, column=3, padx=10, pady=5)
    tk.Label(marco, text="Kg").grid(row=11, column=4, padx=(2, 2), pady=5, sticky="w")

    # Espacio FILA 12
    tk.Label(marco, text="Ubicacion").grid(row=12, column=0, padx=10, pady=5)

    # UBICACION FILA 13
    tk.Label(marco, text="Anaquel:").grid(row=13, column=0, padx=10, pady=5, sticky="e")
    anaqueles = fetch_data("SELECT id_anaquel, nombre FROM anaquel")
    anaquel_combobox = ttk.Combobox(marco, values=[f"{id_} - {nombre}" for id_, nombre in anaqueles])
    anaquel_combobox.grid(row=13, column=1, padx=10, pady=5)

    tk.Label(marco, text="Estante:").grid(row=13, column=2, padx=10, pady=5, sticky="e")
    estantes = fetch_data("SELECT id_estante, nombre FROM estante")
    estante_combobox = ttk.Combobox(marco, values=[f"{id_} - {nombre}" for id_, nombre in estantes])
    estante_combobox.grid(row=13, column=3, padx=10, pady=5)

    tk.Label(marco, text="Cuarto:").grid(row=13, column=4, padx=10, pady=5, sticky="e")
    cuartos = fetch_data("SELECT id_cuarto, nombre FROM cuarto")
    cuarto_combobox = ttk.Combobox(marco, values=[f"{id_} - {nombre}" for id_, nombre in cuartos])
    cuarto_combobox.grid(row=13, column=5, padx=10, pady=5)

    # TECNICA FILA 14
    tk.Label(marco, text="Técnica:").grid(row=14, column=0, padx=10, pady=10, sticky="e")
    tecnicas = fetch_data("SELECT id_tecnica, nombre FROM tecnica")
    tecnica_combobox = ttk.Combobox(marco, values=[f"{id_} - {nombre}" for id_, nombre in tecnicas])
    tecnica_combobox.grid(row=14, column=1, padx=10, pady=10)

    # Espacio FILA 15
    tk.Label(marco, text="Condiciones ambientales").grid(row=15, column=0, padx=10, pady=5)

    # CONDICIONES FILA 16
    tk.Label(marco, text="Temperatura:").grid(row=16, column=0, padx=10, pady=5, sticky="e")
    c_temperatura_entry = tk.Entry(marco)
    c_temperatura_entry.grid(row=16, column=1, padx=10, pady=5)
    tk.Label(marco, text="°C").grid(row=16, column=2, padx=(2, 2), pady=5, sticky="w")

    tk.Label(marco, text="Humedad:").grid(row=16, column=2, padx=10, pady=5, sticky="e")
    c_humedad_entry = tk.Entry(marco)
    c_humedad_entry.grid(row=16, column=3, padx=10, pady=5)
    tk.Label(marco, text="%").grid(row=16, column=4, padx=(2, 2), pady=5, sticky="w")

    tk.Label(marco, text="Oxigenación:").grid(row=16, column=4, padx=10, pady=5, sticky="e")
    c_oxigenacion_entry = tk.Entry(marco)
    c_oxigenacion_entry.grid(row=16, column=5, padx=10, pady=5)
    tk.Label(marco, text="ppm").grid(row=16, column=6, padx=(2, 2), pady=5, sticky="w")

    tk.Button(marco, text="Regresar", command=register_window.destroy).grid(row=17, columnspan=1, pady=10)
    tk.Button(marco, text="Registrar", command=on_registrar).grid(row=17, columnspan=7, pady=10)