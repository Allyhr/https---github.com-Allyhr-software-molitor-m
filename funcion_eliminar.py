import tkinter as tk
import mysql.connector
from tkinter import messagebox, Toplevel, ttk
from funcion_registrar import fetch_data, conectar_bd

def show_delete_unit(root):
    def on_delete():
        selected_item = tree.focus()
        if not selected_item:
            messagebox.showwarning("Eliminar", "Seleccione una unidad para eliminar.")
            return
        
        values = tree.item(selected_item, 'values')
        id_unidad = values[0]
        matricula = values[1]
        
        confirm = messagebox.askyesno("Eliminar", f"¿Está seguro de eliminar la unidad con el ID {matricula}?")
        if confirm:
            try:
                conn = conectar_bd()
                cursor = conn.cursor()
                
                # Iniciar transacción
                conn.start_transaction()
                
                # Eliminar registros dependientes
                cursor.execute("DELETE FROM seguimiento_alimentacion WHERE id_unidad = %s", (id_unidad,))
                cursor.execute("DELETE FROM seguimiento_limpieza WHERE id_unidad = %s", (id_unidad,))
                
                # Eliminar el registro de la tabla unidad
                cursor.execute("DELETE FROM unidad WHERE id_unidad = %s", (id_unidad,))
                
                # Confirmar transacción
                conn.commit()
                
                messagebox.showinfo("Eliminar", "Unidad eliminada exitosamente")
                tree.delete(selected_item)
            except mysql.connector.Error as err:
                # Revertir cambios en caso de error
                conn.rollback()
                messagebox.showerror("Error", f"Error: {err}")
            finally:
                conn.close()

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

    delete_window = Toplevel(root)
    delete_window.title("Eliminar Unidad")

    # Título
    tk.Label(delete_window, text="Eliminación de unidad de cría", fg="black", font=("Comic Sans", 17, "bold"), pady=10).pack()

    # Campo de búsqueda
    search_frame = tk.Frame(delete_window)
    search_frame.pack(fill=tk.X, padx=5, pady=2)

    search_label = tk.Label(search_frame, text="Buscar:")
    search_label.pack(side=tk.LEFT, padx=2)

    search_entry = tk.Entry(search_frame, width=20)
    search_entry.pack(side=tk.LEFT, padx=2)

    search_button = tk.Button(search_frame, text="Buscar", command=on_search)
    search_button.pack(side=tk.LEFT, padx=2)

    # Frame para la tabla y la barra de desplazamiento
    table_frame = tk.Frame(delete_window)
    table_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

    # Estilo para centrar el texto en las columnas
    style = ttk.Style()
    style.configure("Centered.Treeview", anchor="center")

    # Tabla de unidades
    tree = ttk.Treeview(table_frame, columns=("ID", "Matricula"), show='headings', height=10, style="Centered.Treeview")
    tree.heading("ID", text="No.")
    tree.heading("Matricula", text="ID Unidad de cria")
    tree.column("ID", anchor="center")
    tree.column("Matricula", anchor="center")
    tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

    # Barra de desplazamiento
    scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=tree.yview)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    # Configurar la barra de desplazamiento con el Treeview
    tree.configure(yscrollcommand=scrollbar.set)

    rows = fetch_data("SELECT id_unidad, matricula FROM unidad")
    for row in rows:
        tree.insert("", tk.END, values=row)

    # Frame para los botones
    button_frame = tk.Frame(delete_window)
    button_frame.pack(fill=tk.X, padx=5, pady=5)

    # Botón de regresar (ahora a la izquierda)
    close_button = tk.Button(button_frame, text="Regresar", command=delete_window.destroy)
    close_button.pack(side=tk.LEFT, pady=5, padx=5)

    # Botón de eliminar (centrado)
    delete_button = tk.Button(button_frame, text="Eliminar", command=on_delete)
    delete_button.pack(expand=True, pady=5)