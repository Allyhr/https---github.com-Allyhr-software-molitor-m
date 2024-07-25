import tkinter as tk
from tkinter import messagebox
import mysql.connector

def abrir_ventana_configuracion(parent, tipo):
    ventana = tk.Toplevel(parent)
    if tipo == "alimentación":
        ventana.title("Configuracion de alimentacion")
        titulo = "Configuracion de alimentacion"
    else:
        ventana.title("Configuracion de limpieza")
        titulo = "Configuracion de limpieza"
    ventana.configure(bg="white")

    # Título
    tk.Label(ventana, text=titulo, font=("Arial", 16, "bold"), bg="white").pack(pady=(20, 50))
    
    # Frame verde para la configuración
    config_frame = tk.Frame(ventana, bg="#BDDB8C", padx=20, pady=20)
    config_frame.pack(padx=20, pady=20)
    
    entradas = {}
    unidades = {}
    
    if tipo == "alimentación":
        fases = ["Larva - Pequeña", "Larva - Grande", "Imago"]
        campos_bd = ["tiempo_alimentacion_larva_pequena", "tiempo_alimentacion_larva_grande", "tiempo_alimentacion_imago"]
        campos_unidad_bd = ["unidad_tiempo_alim_larva_pequena", "unidad_tiempo_alim_larva_grande", "unidad_tiempo_alim_imago"]
    else:  # limpieza
        fases = ["Larva - Grande", "Pupa", "Imago"]
        campos_bd = ["tiempo_limpieza_larva_grande", "tiempo_limpieza_pupa", "tiempo_limpieza_imago"]
        campos_unidad_bd = ["unidad_tiempo_limp_larva_grande", "unidad_tiempo_limp_pupa", "unidad_tiempo_limp_imago"]

    # Cargar configuración actual
    connection = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="molitorm"
    )
    cursor = connection.cursor(dictionary=True)
    cursor.execute("SELECT * FROM configuracion")
    config_actual = cursor.fetchone()
    connection.close()

    for i, (fase, campo_bd, campo_unidad_bd) in enumerate(zip(fases, campos_bd, campos_unidad_bd)):
        tk.Label(config_frame, text=f"Intervalo de {tipo} ({fase}):", bg="#BDDB8C", anchor="e").grid(row=i, column=0, pady=(0, 10), padx=(0, 10), sticky="e")
        entrada = tk.Entry(config_frame, width=10)
        entrada.insert(0, str(config_actual[campo_bd]))  # Insertar valor actual
        entrada.grid(row=i, column=1, pady=(0, 10), sticky="w")
        unidad_var = tk.StringVar(value=config_actual[campo_unidad_bd])  # Establecer unidad actual
        tk.Radiobutton(config_frame, text="Minutos", variable=unidad_var, value="minutos", bg="#BDDB8C").grid(row=i, column=2, padx=(0, 5))
        tk.Radiobutton(config_frame, text="Horas", variable=unidad_var, value="horas", bg="#BDDB8C").grid(row=i, column=3, padx=(0, 5))
        tk.Radiobutton(config_frame, text="Días", variable=unidad_var, value="dias", bg="#BDDB8C").grid(row=i, column=4)
        entradas[fase] = entrada
        unidades[fase] = unidad_var
    
    def guardar_configuracion():
        try:
            valores = {fase: int(entrada.get()) for fase, entrada in entradas.items()}
            for valor in valores.values():
                if valor <= 0:
                    raise ValueError("Todos los intervalos deben ser números positivos")
            
            connection = mysql.connector.connect(
                host="localhost",
                user="root",
                password="",
                database="molitorm"
            )
            cursor = connection.cursor()
            
            if tipo == "alimentación":
                cursor.execute("""
                    UPDATE configuracion SET 
                    tiempo_alimentacion_larva_pequena = %s,
                    unidad_tiempo_alim_larva_pequena = %s,
                    tiempo_alimentacion_larva_grande = %s,
                    unidad_tiempo_alim_larva_grande = %s,
                    tiempo_alimentacion_imago = %s,
                    unidad_tiempo_alim_imago = %s
                """, (
                    valores["Larva - Pequeña"], unidades["Larva - Pequeña"].get(),
                    valores["Larva - Grande"], unidades["Larva - Grande"].get(),
                    valores["Imago"], unidades["Imago"].get()
                ))
            else:
                cursor.execute("""
                    UPDATE configuracion SET 
                    tiempo_limpieza_larva_grande = %s,
                    unidad_tiempo_limp_larva_grande = %s,
                    tiempo_limpieza_pupa = %s,
                    unidad_tiempo_limp_pupa = %s,
                    tiempo_limpieza_imago = %s,
                    unidad_tiempo_limp_imago = %s
                """, (
                    valores["Larva - Grande"], unidades["Larva - Grande"].get(),
                    valores["Pupa"], unidades["Pupa"].get(),
                    valores["Imago"], unidades["Imago"].get()
                ))
            
            connection.commit()
            connection.close()
            tk.messagebox.showinfo("Éxito", f"Configuración de {tipo} actualizada")
            ventana.destroy()
            parent.cargar_notificaciones()
        except ValueError as e:
            tk.messagebox.showerror("Error", str(e))
    
    tk.Button(config_frame, text="Guardar", command=guardar_configuracion, bg="white").grid(row=len(fases), column=0, columnspan=5, pady=(20, 0))

def configurar_alimentacion(parent):
    abrir_ventana_configuracion(parent, "alimentación")

def configurar_limpieza(parent):
    abrir_ventana_configuracion(parent, "limpieza")