import tkinter as tk
from tkinter import Menu, ttk
from tkinter import messagebox
from PIL import Image, ImageTk
from inicio_sesion import InicioSesion
from funcion_registrar import show_register_unit
from funcion_modificar import show_modify_unit
from funcion_eliminar import show_delete_unit
from barra_usuario import show_register_user
from barra_configuracion import configurar_alimentacion, configurar_limpieza
import mysql.connector
from datetime import datetime, timedelta
import os
import sys

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

class AplicacionPrincipal(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("MolitorMinder")
        self.geometry("800x600")
        
        # Establecer icono de la ventana
        try:
            icon_path = resource_path(os.path.join("images", "icono.ico"))
            self.iconbitmap(icon_path)
        except tk.TclError:
            print("No se pudo cargar el icono de la ventana.")
        
        # Establecer icono de la barra de tareas
        try:
            icon = Image.open(icon_path)
            photo = ImageTk.PhotoImage(icon)
            self.wm_iconphoto(True, photo)
        except Exception as e:
            print(f"No se pudo cargar el icono de la barra de tareas: {e}")
        
        self.scrollable_frames = {}

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        
        self.frame_inicio_sesion = InicioSesion(self, self.on_login_success)
        self.frame_inicio_sesion.grid(row=0, column=0, sticky="nsew")
        
        self.main_frame = tk.Frame(self)
        self.button_frame = tk.Frame(self)
        self.notification_frame = tk.Frame(self)

    def actualizar_fases(self):
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="molitorm"
        )
        cursor = connection.cursor()

        try:
            # Obtener todas las unidades
            cursor.execute("SELECT id_unidad, id_fase, fecha, e_fechaInicio FROM unidad")
            unidades = cursor.fetchall()

            # Obtener la duración de cada fase
            cursor.execute("SELECT id_fase, duracion FROM duracion_fase")
            duraciones = dict(cursor.fetchall())

            for unidad in unidades:
                id_unidad, id_fase, fecha_alta, e_fechaInicio = unidad
                
                # Convertir las fechas a objetos datetime si no lo son ya
                if isinstance(fecha_alta, str):
                    fecha_alta = datetime.strptime(fecha_alta, '%Y-%m-%d').date()
                if isinstance(e_fechaInicio, str):
                    e_fechaInicio = datetime.strptime(e_fechaInicio, '%Y-%m-%d').date()

                # Calcular días transcurridos desde el inicio de la fase actual
                dias_transcurridos = (datetime.now().date() - e_fechaInicio).days

                # Verificar si se debe cambiar de fase
                if dias_transcurridos >= duraciones.get(id_fase, 0) and id_fase < 5:
                    # Calcular la nueva fase
                    nueva_fase = id_fase + 1
                    
                    # Calcular la nueva fecha de inicio de fase
                    nueva_fecha_inicio = e_fechaInicio + timedelta(days=duraciones.get(id_fase, 0))

                    # Actualizar la unidad en la base de datos
                    cursor.execute("""
                        UPDATE unidad 
                        SET id_fase = %s, e_fechaInicio = %s 
                        WHERE id_unidad = %s
                    """, (nueva_fase, nueva_fecha_inicio, id_unidad))

                    # Insertar notificación en la tabla de notificaciones_vistas
                    cursor.execute("""
                        INSERT INTO notificaciones_vistas (id_unidad, tipo_notificacion, fecha_vista)
                        VALUES (%s, %s, %s)
                    """, (id_unidad, 'cambio_fase', datetime.now()))

            connection.commit()

        except mysql.connector.Error as err:
            print(f"Error: {err}")
            messagebox.showerror("Error", "No se pudieron actualizar las fases.")
        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()

        # Actualizar las notificaciones en la interfaz
        self.cargar_notificaciones()

        # Programar la próxima actualización
        self.after(60000, self.actualizar_fases)  # Actualizar cada minuto

    def on_login_success(self):
        # Limpiar widgets existentes
        for widget in self.winfo_children():
            widget.grid_forget()

        self.configure(bg="white")
        self.crear_menu()
        
        # Configurar las filas y columnas del grid
        self.grid_rowconfigure(0, weight=0)  # Fila para imágenes
        self.grid_rowconfigure(1, weight=0)  # Fila para espacio
        self.grid_rowconfigure(2, weight=0)  # Fila para botones
        self.grid_rowconfigure(3, weight=0)  # Fila para espacio
        self.grid_rowconfigure(4, weight=0)  # Fila para notificaciones
        self.grid_rowconfigure(5, weight=0)  # Fila para el contenido principal (espacio flexible)
        self.grid_columnconfigure(0, weight=1)

        # Frame para imágenes
        self.image_frame = tk.Frame(self, bg="white")
        self.image_frame.grid(row=0, column=0, pady=(20, 10), sticky="nw")
        self.cargar_imagenes()
        
        # Espacio entre imágenes y botones
        tk.Frame(self, bg="white", height=20).grid(row=1, column=0)
        
        # Frame para botones
        self.button_frame = tk.Frame(self, bg="white")
        self.button_frame.grid(row=2, column=0, pady=10, sticky="ew")
        
        # Espacio entre botones y notificaciones
        tk.Frame(self, bg="white", height=20).grid(row=3, column=0)
        
        # Frame para notificaciones
        self.notification_frame = tk.Frame(self, bg="white")
        self.notification_frame.grid(row=4, column=0, pady=(10, 20), sticky="ew")
        
        # Frame principal (ahora en la sexta fila)
        self.main_frame = tk.Frame(self, bg="white")
        self.main_frame.grid(row=5, column=0, sticky="nsew")

        self.scrollable_frames = {}
        self.crear_botones()
        self.crear_notificaciones()
        self.cargar_notificaciones()
        self.actualizar_notificaciones_periodicamente()

        # Iniciar la actualización automática de fases
        self.actualizar_fases()

    def actualizar_notificaciones_periodicamente(self):
        self.cargar_notificaciones()
        # Programar la próxima actualización
        self.after(60000, self.actualizar_notificaciones_periodicamente)
    
    def actualizar_select_all(self, frame_name):
        frame = self.scrollable_frames[frame_name]
        select_all_var = self.select_all_vars[frame_name]
        
        # Verificar si todas las tareas están completadas
        todas_completadas = all(isinstance(widget, tk.Checkbutton) and not widget.winfo_exists() for widget in frame.winfo_children())
        
        # Actualizar el estado del checkbox "Seleccionar todas"
        select_all_var.set(todas_completadas)
    
    def cargar_imagenes(self):
        # Cargar y mostrar las imágenes
        img1_path = resource_path(os.path.join("images", "icono1.png"))
        img2_path = resource_path(os.path.join("images", "Imagen3.png"))
        
        img1 = Image.open(img1_path)
        img2 = Image.open(img2_path)
        
        # Redimensionar las imágenes si es necesario
        img1 = img1.resize((100, 100))  # Ajusta el tamaño según tus necesidades
        img2 = img2.resize((260, 90))  # Ajusta el tamaño según tus necesidades
        
        self.photo1 = ImageTk.PhotoImage(img1)
        self.photo2 = ImageTk.PhotoImage(img2)
        
        label1 = tk.Label(self.image_frame, image=self.photo1, bg="white")
        label1.grid(row=0, column=0, padx=(10, 5))
        
        label2 = tk.Label(self.image_frame, image=self.photo2, bg="white")
        label2.grid(row=0, column=1, padx=(5, 10))

    def crear_menu(self):
        menu_bar = Menu(self)
        self.config(menu=menu_bar)

        file_menu = Menu(menu_bar, tearoff=0)
        menu_bar.add_cascade(label="Inicio", menu=file_menu)
        file_menu.add_command(label="Inicio", command=self.volver_a_inicio) 

        edit_menu = Menu(menu_bar, tearoff=0)
        menu_bar.add_cascade(label="Configurar", menu=edit_menu)
        edit_menu.add_command(label="Configuración de alimentación", command=lambda: configurar_alimentacion(self))
        edit_menu.add_command(label="Configuración de limpieza", command=lambda: configurar_limpieza(self))

        user_menu = Menu(menu_bar, tearoff=0)
        menu_bar.add_cascade(label="Registrar usuario", menu=user_menu)
        user_menu.add_command(label="Nuevo usuario", command=self.mostrar_registro_usuario)

        logout_menu = Menu(menu_bar, tearoff=0)
        menu_bar.add_cascade(label="Cerrar sesión", menu=logout_menu)
        logout_menu.add_command(label="Cerrar sesión", command=self.cerrar_sesion)  

    def cerrar_sesion(self):
        # Destruir todos los widgets
        for widget in self.winfo_children():
            widget.destroy()
        
        # Eliminar la barra de menú
        self.config(menu="")
        
        # Reconfigurar el grid
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        
        # Crear y mostrar la nueva pantalla de inicio de sesión
        self.frame_inicio_sesion = InicioSesion(self, self.on_login_success)
        self.frame_inicio_sesion.grid(row=0, column=0, sticky="nsew")
    
    def volver_a_inicio(self):
        # Ocultar el frame de registro de usuario si existe
        if hasattr(self, 'registro_usuario_frame'):
            self.registro_usuario_frame.grid_remove()
        
        # Limpiar el main_frame
        for widget in self.main_frame.winfo_children():
            widget.destroy()

        # Frame para imágenes
        self.image_frame = tk.Frame(self, bg="white")
        self.image_frame.grid(row=0, column=0, pady=(20, 10), sticky="nw")
        self.cargar_imagenes()
        
        # Espacio entre imágenes y botones
        tk.Frame(self, bg="white", height=20).grid(row=1, column=0)
        
        # Frame para botones
        self.button_frame = tk.Frame(self, bg="white")
        self.button_frame.grid(row=2, column=0, pady=10, sticky="ew")
        
        # Espacio entre botones y notificaciones
        tk.Frame(self, bg="white", height=20).grid(row=3, column=0)
        
        # Frame para notificaciones
        self.notification_frame = tk.Frame(self, bg="white")
        self.notification_frame.grid(row=4, column=0, pady=(10, 20), sticky="ew")
        
        # Frame principal (ahora en la sexta fila)
        self.main_frame = tk.Frame(self, bg="white")
        self.main_frame.grid(row=5, column=0, sticky="nsew")
        
        # Recargar las imágenes, botones y notificaciones

        self.scrollable_frames = {}
        self.crear_botones()
        self.crear_notificaciones()
        self.cargar_notificaciones()
        self.actualizar_notificaciones_periodicamente()

    def crear_botones(self):
        self.button_frame.grid_columnconfigure((0, 1, 2, 3, 4, 5, 6), weight=1)
        
        registrarunidad_button = tk.Button(self.button_frame, text="Registrar unidad", command=self.registrar_unidad)
        registrarunidad_button.grid(row=0, column=2, padx=2, pady=50)

        modificar_button = tk.Button(self.button_frame, text="Modificar unidad", command=self.modificar_unidad)
        modificar_button.grid(row=0, column=3, padx=2, pady=50)

        eliminar_button = tk.Button(self.button_frame, text="Eliminar unidad", command=self.eliminar_unidad)
        eliminar_button.grid(row=0, column=4, padx=2, pady=50)
        
    def crear_notificaciones(self):
        self.notification_frame.grid_columnconfigure((0, 1, 2), weight=1)
        
        self.scrollable_frames = {}
        self.select_all_vars = {}
        
        for frame_name, title in [
            ("alimentacion", "Notificaciones de Alimentación"),
            ("limpieza", "Notificaciones de Limpieza"),
            ("fases", "Cambio de Estadio")
        ]:
            frame = ttk.LabelFrame(self.notification_frame, text=title)
            frame.grid(row=0, column=list(self.scrollable_frames.keys()).index(frame_name) if frame_name in self.scrollable_frames else len(self.scrollable_frames), 
                    padx=5, sticky="nsew")

            # Agregar checkbox "Seleccionar todas" para todos los tipos de notificaciones
            select_all_var = tk.BooleanVar()
            select_all_checkbox = tk.Checkbutton(frame, text="Seleccionar todas", variable=select_all_var, 
                                                command=lambda fn=frame_name: self.toggle_all_tasks(fn))
            select_all_checkbox.pack(anchor="w")
            self.select_all_vars[frame_name] = select_all_var

            canvas = tk.Canvas(frame, width=50, height=150)
            scrollbar = ttk.Scrollbar(frame, orient="vertical", command=canvas.yview)
            scrollable_frame = ttk.Frame(canvas)

            scrollable_frame.bind(
                "<Configure>",
                lambda e, canvas=canvas: canvas.configure(
                    scrollregion=canvas.bbox("all")
                )
            )

            canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
            canvas.configure(yscrollcommand=scrollbar.set)

            canvas.pack(side="left", fill="both", expand=True)
            scrollbar.pack(side="right", fill="y")

            self.scrollable_frames[frame_name] = scrollable_frame

        # Cargar notificaciones
        self.cargar_notificaciones()

        # Configurar actualización periódica de notificaciones
        self.after(60000, self.actualizar_notificaciones_periodicamente)

    def toggle_all_tasks(self, frame_name):
        select_all_var = self.select_all_vars[frame_name]
        frame = self.scrollable_frames[frame_name]
        
        if select_all_var.get():
            # Recopilar todas las tareas pendientes
            tareas_pendientes = [widget for widget in frame.winfo_children() if isinstance(widget, tk.Checkbutton)]
            
            # Marcar todas las tareas como completadas
            for checkbox in tareas_pendientes:
                self.marcar_completado(checkbox.id_unidad, checkbox.tipo, checkbox.label, checkbox)
            
            # Desmarcar el checkbox "Seleccionar todas" después de completar todas las tareas
            self.after(100, lambda: select_all_var.set(False))
        
        # Actualizar las notificaciones
        self.cargar_notificaciones()

    def cargar_notificaciones(self):
        print("Iniciando carga de notificaciones")
        if not hasattr(self, 'scrollable_frames') or not self.scrollable_frames:
            print("Los frames de notificaciones aún no están inicializados.")
            return

        # Limpiar notificaciones existentes
        for frame in self.scrollable_frames.values():
            for widget in frame.winfo_children():
                widget.destroy()

        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="molitorm"
        )
        cursor = connection.cursor()

        try:
            # Cargar notificaciones de alimentación para id_fase 2, 3 y 5
            print("Cargando notificaciones de alimentación")
            cursor.execute("""
                SELECT u.id_unidad, u.matricula, s.proxima_alimentacion, u.id_fase
                FROM unidad u 
                JOIN seguimiento_alimentacion s ON u.id_unidad = s.id_unidad 
                WHERE s.proxima_alimentacion <= NOW() 
                AND u.id_fase IN (2, 3, 5)
            """)
            notificaciones_alimentacion = cursor.fetchall()
            for i, (id_unidad, matricula, proxima_alimentacion, id_fase) in enumerate(notificaciones_alimentacion):
                fase_texto = "Larva - Pequeña" if id_fase == 2 else "Larva - Grande" if id_fase == 3 else "Imago"
                self.crear_notificacion(self.scrollable_frames['alimentacion'], i, id_unidad, matricula, proxima_alimentacion, f"alimentación ({fase_texto})")
            print(f"Se cargaron {len(notificaciones_alimentacion)} notificaciones de alimentación")

            # Cargar notificaciones de limpieza para id_fase 3, 4 y 5
            print("Cargando notificaciones de limpieza")
            cursor.execute("""
                SELECT u.id_unidad, u.matricula, s.proxima_limpieza, u.id_fase
                FROM unidad u 
                JOIN seguimiento_limpieza s ON u.id_unidad = s.id_unidad 
                WHERE s.proxima_limpieza <= NOW() 
                AND u.id_fase IN (3, 4, 5)
            """)
            notificaciones_limpieza = cursor.fetchall()
            for i, (id_unidad, matricula, proxima_limpieza, id_fase) in enumerate(notificaciones_limpieza):
                fase_texto = "Larva - Grande" if id_fase == 3 else "Pupa" if id_fase == 4 else "Imago"
                self.crear_notificacion(self.scrollable_frames['limpieza'], i, id_unidad, matricula, proxima_limpieza, f"limpieza ({fase_texto})")
            print(f"Se cargaron {len(notificaciones_limpieza)} notificaciones de limpieza")

            # Cargar notificaciones de cambio de fase
            print("Cargando notificaciones de cambio de fase")
            cursor.execute("""
                SELECT n.id_unidad, u.matricula, n.fecha_vista, u.id_fase
                FROM notificaciones_vistas n
                JOIN unidad u ON n.id_unidad = u.id_unidad
                WHERE n.tipo_notificacion = 'cambio_fase'
                AND n.fecha_vista > DATE_SUB(NOW(), INTERVAL 1 DAY)
            """)
            notificaciones_cambio_fase = cursor.fetchall()
            for i, (id_unidad, matricula, fecha_vista, id_fase) in enumerate(notificaciones_cambio_fase):
                fase_texto = "Huevo" if id_fase == 1 else "Larva - Pequeña" if id_fase == 2 else "Larva - Grande" if id_fase == 3 else "Pupa" if id_fase == 4 else "Imago"
                self.crear_notificacion(self.scrollable_frames['fases'], i, id_unidad, matricula, fecha_vista, f"cambio a estadio {fase_texto}")
            print(f"Se cargaron {len(notificaciones_cambio_fase)} notificaciones de cambio de fase")

            # Actualizar la interfaz
            self.update_idletasks()
            print("Interfaz actualizada")

        except mysql.connector.Error as err:
            print(f"Error MySQL: {err}")
            messagebox.showerror("Error", f"No se pudieron cargar las notificaciones: {err}")
        except Exception as e:
            print(f"Error inesperado: {e}")
            messagebox.showerror("Error", f"Error inesperado al cargar notificaciones: {e}")
        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()
            print("Conexión cerrada.")

        # Actualizar la interfaz
        self.update_idletasks()
        print("Carga de notificaciones completada")
    
    def crear_notificacion(self, frame, row, id_unidad, matricula, fecha, tipo):
        label = tk.Label(frame, text=f"Unidad con ID: {matricula}: {tipo.capitalize()}")
        label.grid(row=row, column=0, padx=5, pady=2, sticky="w")

        checkbox = tk.Checkbutton(frame, command=lambda: self.marcar_completado(id_unidad, tipo, label, checkbox))
        checkbox.grid(row=row, column=1, padx=5, pady=2)
        checkbox.label = label
        checkbox.id_unidad = id_unidad
        checkbox.tipo = tipo

    def marcar_completado(self, id_unidad, tipo, label, checkbox):
        print(f"Iniciando marcar_completado: id_unidad={id_unidad}, tipo={tipo}")
        
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="molitorm"
        )
        cursor = connection.cursor()

        now = datetime.now()
        
        try:
            if tipo.startswith("cambio a estadio"):
                print(f"Procesando cambio de fase para unidad {id_unidad}")
                cursor.execute("""
                    DELETE FROM notificaciones_vistas
                    WHERE id_unidad = %s AND tipo_notificacion = 'cambio_fase'
                """, (id_unidad,))
                print(f"Notificación de cambio de fase eliminada para unidad {id_unidad}")
            
            elif tipo.startswith("alimentación") or tipo.startswith("limpieza"):
                # Obtener la fase actual de la unidad
                cursor.execute("SELECT id_fase FROM unidad WHERE id_unidad = %s", (id_unidad,))
                result = cursor.fetchone()
                if not result:
                    raise ValueError(f"No se encontró la unidad con id {id_unidad}")
                id_fase = result[0]

                # Construir la consulta SQL basada en el tipo y la fase
                if tipo.startswith("alimentación"):
                    if id_fase == 2:
                        query = "SELECT tiempo_alimentacion_larva_pequena, unidad_tiempo_alim_larva_pequena FROM configuracion"
                    elif id_fase == 3:
                        query = "SELECT tiempo_alimentacion_larva_grande, unidad_tiempo_alim_larva_grande FROM configuracion"
                    elif id_fase == 5:
                        query = "SELECT tiempo_alimentacion_imago, unidad_tiempo_alim_imago FROM configuracion"
                    else:
                        raise ValueError(f"Fase no válida para alimentación: {id_fase}")
                else:  # limpieza
                    if id_fase == 3:
                        query = "SELECT tiempo_limpieza_larva_grande, unidad_tiempo_limp_larva_grande FROM configuracion"
                    elif id_fase == 4:
                        query = "SELECT tiempo_limpieza_pupa, unidad_tiempo_limp_pupa FROM configuracion"
                    elif id_fase == 5:
                        query = "SELECT tiempo_limpieza_imago, unidad_tiempo_limp_imago FROM configuracion"
                    else:
                        raise ValueError(f"Fase no válida para limpieza: {id_fase}")

                cursor.execute(query)
                result = cursor.fetchone()
                if not result:
                    raise ValueError("No se encontró configuración en la base de datos")
                
                tiempo, unidad = result

                if unidad == 'minutos':
                    proxima = now + timedelta(minutes=tiempo)
                elif unidad == 'horas':
                    proxima = now + timedelta(hours=tiempo)
                else:  # dias
                    proxima = now + timedelta(days=tiempo)
                
                if tipo.startswith("alimentación"):
                    cursor.execute("UPDATE seguimiento_alimentacion SET ultima_alimentacion = %s, proxima_alimentacion = %s WHERE id_unidad = %s", (now, proxima, id_unidad))
                else:
                    cursor.execute("UPDATE seguimiento_limpieza SET ultima_limpieza = %s, proxima_limpieza = %s WHERE id_unidad = %s", (now, proxima, id_unidad))

            else:
                print(f"Tipo de notificación no reconocido: {tipo}")
                return

            connection.commit()
            print(f"Operación completada exitosamente para unidad {id_unidad}, tipo {tipo}")
            
            # Eliminar la notificación de la interfaz
            if label and label.winfo_exists():
                label.destroy()
            if checkbox and checkbox.winfo_exists():
                checkbox.destroy()
            
            # Actualizar el estado del checkbox "Seleccionar todas"
            frame_name = 'alimentacion' if tipo.startswith("alimentación") else 'limpieza' if tipo.startswith("limpieza") else 'fases'
            self.actualizar_select_all(frame_name)
            
            # Recargar las notificaciones
            self.cargar_notificaciones()
            
        except mysql.connector.Error as err:
            print(f"Error MySQL: {err}")
            messagebox.showerror("Error", f"Error de base de datos: {err}")
        except ValueError as ve:
            print(f"Error de valor: {ve}")
            messagebox.showerror("Error", str(ve))
        except Exception as e:
            print(f"Error inesperado: {e}")
            messagebox.showerror("Error", f"Error inesperado: {e}")
        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()
            print("Conexión cerrada.")
    
    def mostrar_registro_usuario(self):
        # Ocultar los elementos del inicio
        self.image_frame.grid_remove()
        self.button_frame.grid_remove()
        self.notification_frame.grid_remove()
        self.main_frame.grid_remove()

        # Crear y mostrar el frame de registro de usuario
        self.registro_usuario_frame = tk.Frame(self)
        self.registro_usuario_frame.grid(row=0, column=0, sticky="nsew")
        
        # Llamar a show_register_user con el frame de registro de usuario y capturar las entradas
        self.registro_entries = show_register_user(self.registro_usuario_frame)

    def registrar_unidad(self):
        show_register_unit(self)

    def modificar_unidad(self):
        show_modify_unit(self)

    def eliminar_unidad(self):
        show_delete_unit(self)

    def opcion_genérica(self):
        print("Opción de menú seleccionada")

if __name__ == "__main__":
    app = AplicacionPrincipal()
    app.mainloop()
