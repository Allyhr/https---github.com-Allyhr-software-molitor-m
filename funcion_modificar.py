import mysql.connector
from tkinter import messagebox, Toplevel, ttk
import tkinter as tk
import datetime
from funcion_registrar import fetch_data, conectar_bd

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
        
        self.set(current_date)
    
    def get(self):
        return f"{self.year_var.get()}-{self.month_var.get().zfill(2)}-{self.day_var.get().zfill(2)}"
    
    def set(self, date):
        if isinstance(date, str):
            date = datetime.datetime.strptime(date, "%Y-%m-%d").date()
        self.year_var.set(date.year)
        self.month_var.set(f"{date.month:02d}")
        self.day_var.set(f"{date.day:02d}")
    
    def delete(self, first, last=None):
        # Esta función no hace nada realmente, pero evita el error
        pass
    
    def insert(self, index, string):
        # Asumimos que el string es una fecha en formato "YYYY-MM-DD"
        self.set(string)

def show_modify_unit(root):
    def on_update():
        datos = {
            "id_unidad": id_unidad_entry.get(),
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
        update_unit(datos, modify_window)

    def update_unit(datos, modify_window):
        try:
            conn = conectar_bd()
            cursor = conn.cursor()
            query = """
            UPDATE unidad SET matricula=%(matricula)s, fecha=%(fecha)s, id_fase=%(id_fase)s, e_fechaInicio=%(e_fechaInicio)s, 
            e_semana=%(e_semana)s, d_ancho=%(d_ancho)s, d_largo=%(d_largo)s, d_alto=%(d_alto)s, biomasa=%(biomasa)s, 
            id_alimentoh=%(id_alimentoh)s, peso_alimentoh=%(peso_alimentoh)s, id_sustrato=%(id_sustrato)s, peso_sustrato=%(peso_sustrato)s, 
            id_anaquel=%(id_anaquel)s, id_estante=%(id_estante)s, id_cuarto=%(id_cuarto)s, id_tecnica=%(id_tecnica)s, 
            c_temperatura=%(c_temperatura)s, c_humedad=%(c_humedad)s, c_oxigenacion=%(c_oxigenacion)s WHERE id_unidad=%(id_unidad)s
            """
            cursor.execute(query, datos)
            conn.commit()
            conn.close()
            messagebox.showinfo("Éxito", "Unidad actualizada exitosamente")
            modify_window.destroy()
        except mysql.connector.Error as err:
            messagebox.showerror("Error", f"Error: {err}")

    def on_select(event):
        selected_item = tree.focus()
        values = tree.item(selected_item, 'values')
        id_unidad_entry.config(state=tk.NORMAL)
        id_unidad_entry.delete(0, tk.END)
        id_unidad_entry.insert(0, values[0])
        id_unidad_entry.config(state='readonly')

        matricula_entry.delete(0, tk.END)
        matricula_entry.insert(0, values[1])

        unidad = fetch_data(f"SELECT * FROM unidad WHERE id_unidad={values[0]}")[0]

        fecha_entry.set(unidad[2])  # Usar set en lugar de delete e insert

        fase_combobox.set(f"{unidad[3]} - {fetch_data(f'SELECT nombre FROM fase WHERE id_fase={unidad[3]}')[0][0]}")

        e_fechaInicio_entry.set(unidad[4])  # Usar set en lugar de delete e insert

        e_semana_combobox.set(unidad[5])

        d_ancho_entry.delete(0, tk.END)
        d_ancho_entry.insert(0, unidad[6])

        d_largo_entry.delete(0, tk.END)
        d_largo_entry.insert(0, unidad[7])

        d_alto_entry.delete(0, tk.END)
        d_alto_entry.insert(0, unidad[8])

        biomasa_entry.delete(0, tk.END)
        biomasa_entry.insert(0, unidad[9])

        alimentoh_combobox.set(
            f"{unidad[10]} - {fetch_data(f'SELECT nombre FROM alimentoh WHERE id_alimentoh={unidad[10]}')[0][0]}")

        peso_alimentoh_entry.delete(0, tk.END)
        peso_alimentoh_entry.insert(0, unidad[11])

        sustrato_combobox.set(
            f"{unidad[12]} - {fetch_data(f'SELECT nombre FROM sustrato WHERE id_sustrato={unidad[12]}')[0][0]}")

        peso_sustrato_entry.delete(0, tk.END)
        peso_sustrato_entry.insert(0, unidad[13])

        anaquel_combobox.set(
            f"{unidad[14]} - {fetch_data(f'SELECT nombre FROM anaquel WHERE id_anaquel={unidad[14]}')[0][0]}")

        estante_combobox.set(
            f"{unidad[15]} - {fetch_data(f'SELECT nombre FROM estante WHERE id_estante={unidad[15]}')[0][0]}")

        cuarto_combobox.set(
            f"{unidad[16]} - {fetch_data(f'SELECT nombre FROM cuarto WHERE id_cuarto={unidad[16]}')[0][0]}")

        tecnica_combobox.set(
            f"{unidad[17]} - {fetch_data(f'SELECT nombre FROM tecnica WHERE id_tecnica={unidad[17]}')[0][0]}")

        c_temperatura_entry.delete(0, tk.END)
        c_temperatura_entry.insert(0, unidad[18])

        c_humedad_entry.delete(0, tk.END)
        c_humedad_entry.insert(0, unidad[19])

        c_oxigenacion_entry.delete(0, tk.END)
        c_oxigenacion_entry.insert(0, unidad[20])

    def on_search():
        query = search_entry.get()
        if query:
            query = f"%{query}%"
            rows = fetch_data(f"""
                SELECT id_unidad, matricula 
                FROM unidad 
                WHERE id_unidad LIKE '{query}' 
                OR matricula LIKE '{query}' 
                OR id_fase IN (SELECT id_fase FROM fase WHERE nombre LIKE '{query}')
            """)
        else:
            rows = fetch_data("SELECT id_unidad, matricula FROM unidad")

        for item in tree.get_children():
            tree.delete(item)

        for row in rows:
            tree.insert("", tk.END, values=row)

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

    modify_window = Toplevel(root)
    modify_window.title("Modificar Unidad")

    # Título
    tk.Label(modify_window, text="Modificación de unidad de cría", fg="black", font=("Comic Sans", 17, "bold"), pady=10).pack()

    # Campo de búsqueda
    search_frame = tk.Frame(modify_window)
    search_frame.pack(fill=tk.X, padx=5, pady=2)

    search_label = tk.Label(search_frame, text="Buscar:")
    search_label.pack(side=tk.LEFT, padx=2)

    search_entry = tk.Entry(search_frame, width=20)
    search_entry.pack(side=tk.LEFT, padx=2)

    search_button = tk.Button(search_frame, text="Buscar", command=on_search)
    search_button.pack(side=tk.LEFT, padx=2)

    # Crear un frame para contener el Treeview y el Scrollbar
    tree_frame = tk.Frame(modify_window)
    tree_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(40, 0))

    # Crear el Scrollbar
    scrollbar = ttk.Scrollbar(tree_frame, orient="vertical")
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    # Crear el Treeview
    tree = ttk.Treeview(tree_frame, columns=("ID", "Matricula"), show='headings', height=5,
                        yscrollcommand=scrollbar.set)
    tree.heading("ID", text="No.")
    tree.heading("Matricula", text="ID Unidad de cria")
    tree.column("ID", width=50)
    tree.column("Matricula", width=80)
    tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

    # Configurar el Scrollbar para controlar el Treeview
    scrollbar.config(command=tree.yview)

    style = ttk.Style()
    style.configure("Treeview", rowheight=16)

    for row in fetch_data("SELECT id_unidad, matricula FROM unidad"):
        tree.insert("", tk.END, values=row)

    tree.bind("<<TreeviewSelect>>", on_select)

    # Formulario de modificación (lado derecho)
    marco = tk.LabelFrame(modify_window, text="Modificar Unidad", font=("Comic Sans", 10, "bold"), pady=5)
    marco.config(bd=2)
    marco.pack(side=tk.RIGHT, padx=10, pady=10)

    # No. FILA 0
    tk.Label(marco, text="No.:").grid(row=0, column=0, padx=10, pady=5, sticky="e")
    id_unidad_entry = tk.Entry(marco)
    id_unidad_entry.grid(row=0, column=1, padx=10, pady=5)
    id_unidad_entry.config(state='readonly')

    # ID FILA 1
    tk.Label(marco, text="ID de la unidad de cria:").grid(row=1, column=0, padx=10, pady=5, sticky="e")
    matricula_entry = tk.Entry(marco)
    matricula_entry.grid(row=1, column=1, padx=10, pady=5)

    # FECHA FILA 1
    tk.Label(marco, text="Fecha de alta a unidad de cria:").grid(row=1, column=2, padx=10, pady=5, sticky="e")
    fecha_entry = DateEntry(marco)
    fecha_entry.grid(row=1, column=3, padx=10, pady=5)

    # Espacio FILA 2
    tk.Label(marco, text="").grid(row=2, column=0, padx=10, pady=5)

    # ESTADIO FILA 3
    tk.Label(marco, text="Estadio:").grid(row=3, column=0, padx=10, pady=5, sticky="e")
    fases = fetch_data("SELECT id_fase, nombre FROM fase")
    fase_combobox = ttk.Combobox(marco, values=[f"{id_} - {nombre}" for id_, nombre in fases])
    fase_combobox.grid(row=3, column=1, padx=10, pady=5)

    # FECHA FILA 3
    tk.Label(marco, text="Fecha de estadio:").grid(row=3, column=2, padx=10, pady=5, sticky="e")
    e_fechaInicio_entry = DateEntry(marco)
    e_fechaInicio_entry.grid(row=3, column=3, padx=10, pady=5)

    # SEMANA FILA 3
    tk.Label(marco, text="Semana(s):").grid(row=3, column=4, padx=10, pady=5, sticky="e")
    e_semana_combobox = ttk.Combobox(marco, values=[str(i) for i in range(17)], state="readonly")
    e_semana_combobox.grid(row=3, column=5, padx=10, pady=5)

    # DIMENSIONES FILA 4
    tk.Label(marco, text="Dimensiones de la unidad de cria").grid(row=4, column=0, padx=10, pady=5)

    # ANCHO FILA 5
    tk.Label(marco, text="Ancho:").grid(row=5, column=0, padx=10, pady=5, sticky="e")
    d_ancho_entry = tk.Entry(marco)
    d_ancho_entry.grid(row=5, column=1, padx=10, pady=5)
    tk.Label(marco, text="cm").grid(row=5, column=2, padx=(2, 2), pady=5, sticky="w")

    # LARGO FILA 5
    tk.Label(marco, text="Largo:").grid(row=5, column=2, padx=10, pady=5, sticky="e")
    d_largo_entry = tk.Entry(marco)
    d_largo_entry.grid(row=5, column=3, padx=10, pady=5)
    tk.Label(marco, text="cm").grid(row=5, column=4, padx=(2, 2), pady=5, sticky="w")

    # ALTO FILA 5
    tk.Label(marco, text="Alto:").grid(row=5, column=4, padx=10, pady=5, sticky="e")
    d_alto_entry = tk.Entry(marco)
    d_alto_entry.grid(row=5, column=5, padx=10, pady=5)
    tk.Label(marco, text="cm").grid(row=5, column=6, padx=(2, 2), pady=5, sticky="w")

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

    # ALIMENTO HUMEDO FILA 9
    tk.Label(marco, text="Alimento húmedo:").grid(row=9, column=0, padx=10, pady=5, sticky="e")
    alimentoh = fetch_data("SELECT id_alimentoh, nombre FROM alimentoh")
    alimentoh_combobox = ttk.Combobox(marco, values=[f"{id_} - {nombre}" for id_, nombre in alimentoh])
    alimentoh_combobox.grid(row=9, column=1, padx=10, pady=5)

    tk.Label(marco, text="Peso del alimento húmedo:").grid(row=9, column=2, padx=10, pady=5, sticky="e")
    peso_alimentoh_entry = tk.Entry(marco)
    peso_alimentoh_entry.grid(row=9, column=3, padx=10, pady=5)
    tk.Label(marco, text="Kg").grid(row=9, column=4, padx=(2, 2), pady=5, sticky="w")

    # SUSTRATO FILA 10
    tk.Label(marco, text="Sustrato:").grid(row=10, column=0, padx=10, pady=5, sticky="e")
    sustratos = fetch_data("SELECT id_sustrato, nombre FROM sustrato")
    sustrato_combobox = ttk.Combobox(marco, values=[f"{id_} - {nombre}" for id_, nombre in sustratos])
    sustrato_combobox.grid(row=10, column=1, padx=10, pady=5)

    tk.Label(marco, text="Peso del sustrato:").grid(row=10, column=2, padx=10, pady=5, sticky="e")
    peso_sustrato_entry = tk.Entry(marco)
    peso_sustrato_entry.grid(row=10, column=3, padx=10, pady=5)
    tk.Label(marco, text="Kg").grid(row=10, column=4, padx=(2, 2), pady=5, sticky="w")

    # UBICACION FILA 11
    tk.Label(marco, text="Ubicacion").grid(row=11, column=0, padx=10, pady=5)

    # ANAQUEL FILA 12
    tk.Label(marco, text="Anaquel:").grid(row=12, column=0, padx=10, pady=5, sticky="e")
    anaqueles = fetch_data("SELECT id_anaquel, nombre FROM anaquel")
    anaquel_combobox = ttk.Combobox(marco, values=[f"{id_} - {nombre}" for id_, nombre in anaqueles])
    anaquel_combobox.grid(row=12, column=1, padx=10, pady=5)

    # ESTANTE FILA 12
    tk.Label(marco, text="Estante:").grid(row=12, column=2, padx=10, pady=5, sticky="e")
    estantes = fetch_data("SELECT id_estante, nombre FROM estante")
    estante_combobox = ttk.Combobox(marco, values=[f"{id_} - {nombre}" for id_, nombre in estantes])
    estante_combobox.grid(row=12, column=3, padx=10, pady=5)

    # CUARTO FILA 12
    tk.Label(marco, text="Cuarto:").grid(row=12, column=4, padx=10, pady=5, sticky="e")
    cuartos = fetch_data("SELECT id_cuarto, nombre FROM cuarto")
    cuarto_combobox = ttk.Combobox(marco, values=[f"{id_} - {nombre}" for id_, nombre in cuartos])
    cuarto_combobox.grid(row=12, column=5, padx=10, pady=5)

    # TECNICA FILA 13
    tk.Label(marco, text="Tecnica:").grid(row=13, column=0, padx=10, pady=5, sticky="e")
    tecnicas = fetch_data("SELECT id_tecnica, nombre FROM tecnica")
    tecnica_combobox = ttk.Combobox(marco, values=[f"{id_} - {nombre}" for id_, nombre in tecnicas])
    tecnica_combobox.grid(row=13, column=1, padx=10, pady=5)

    # Espacio FILA 14
    tk.Label(marco, text="").grid(row=14, column=0, padx=10, pady=5)

    # Condiciones FILA 15
    tk.Label(marco, text="Condiciones ambientales").grid(row=15, column=0, padx=10, pady=5)

    tk.Label(marco, text="Temperatura:").grid(row=16, column=0, padx=10, pady=5, sticky="e")
    c_temperatura_entry = tk.Entry(marco)
    c_temperatura_entry.grid(row=16, column=1, padx=10, pady=5)
    tk.Label(marco, text="°C").grid(row=16, column=2, padx=(2, 2), pady=5, sticky="w")

    tk.Label(marco, text="Humedad:").grid(row=16, column=2, padx=10, pady=5, sticky="e")
    c_humedad_entry = tk.Entry(marco)
    c_humedad_entry.grid(row=16, column=3, padx=10, pady=5)
    tk.Label(marco, text="%").grid(row=16, column=4, padx=(2, 2), pady=5, sticky="w")

    tk.Label(marco, text="Oxigenación:").grid(row=16, column=4, padx=25, pady=5, sticky="e")
    c_oxigenacion_entry = tk.Entry(marco)
    c_oxigenacion_entry.grid(row=16, column=5, padx=10, pady=5)
    tk.Label(marco, text="ppm").grid(row=16, column=6, padx=(2, 2), pady=5, sticky="w")

    tk.Button(marco, text="Modificar", command=on_update).grid(row=17, column=0, columnspan=6, pady=10)