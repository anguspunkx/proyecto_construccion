"""
Sistema de Cálculo de Costos de Construcción
Archivo: interfaz.py
Interfaz gráfica principal con tkinter
"""

import tkinter as tk
import db  # Importar el módulo de base de datos
from tkinter import ttk, messagebox, simpledialog
from clases import Casa, Habitacion
from datos import (
    listar_nombres_materiales_piso,
    listar_nombres_materiales_pared,
    listar_nombres_sistemas,
    listar_tipos_habitacion,
    obtener_material_piso,
    obtener_material_pared,
    obtener_sistema_construccion,
    obtener_dimensiones_tipo,
    formatear_precio,
    TIPOS_HABITACION
)

class InterfazPrincipal:
    """Interfaz gráfica principal del sistema"""
    
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Sistema de Cálculo de Costos de Construcción")
        self.root.geometry("1280x820")
        self.root.configure(bg='#e9ecef')
        self.root.minsize(1100, 700)

        # Paleta de colores profesional
        self.color_primario = "#2E86AB"
        self.color_secundario = "#F5F6FA"
        self.color_acento = "#4ECDC4"
        self.color_texto = "#22223B"
        self.color_panel = "#FFFFFF"

        # Datos principales
        self.casa_actual = Casa("Mi Casa")  # Siempre inicializar con una casa por defecto
        self.casa_id = None
        self.habitacion_seleccionada = None

        # Configurar estilo
        self.configurar_estilo()

        # Crear interfaz
        self.crear_interfaz()

        # Seleccionar casa al iniciar
        self.seleccionar_casa_al_iniciar()

        # Actualizar vista inicial
        self.actualizar_lista_habitaciones()
        self.actualizar_resumen()

    def configurar_estilo(self):
        """Configura el estilo de la interfaz"""
        style = ttk.Style()
        style.theme_use('clam')

        # Colores y fuentes
        style.configure('TFrame', background=self.color_panel)
        style.configure('Title.TLabel', font=('Segoe UI', 22, 'bold'), foreground=self.color_primario, background=self.color_secundario)
        style.configure('Header.TLabel', font=('Segoe UI', 14, 'bold'), foreground=self.color_texto, background=self.color_panel)
        style.configure('Subtitle.TLabel', font=('Segoe UI', 12, 'bold'), foreground=self.color_primario, background=self.color_panel)
        style.configure('Info.TLabel', font=('Segoe UI', 10), foreground='#666', background=self.color_panel)
        style.configure('Success.TLabel', font=('Segoe UI', 10), foreground='#28a745', background=self.color_panel)
        style.configure('Error.TLabel', font=('Segoe UI', 10), foreground='#dc3545', background=self.color_panel)
        style.configure('TButton', font=('Segoe UI', 11, 'bold'), padding=8, background=self.color_primario, foreground='white')
        style.map('TButton', background=[('active', self.color_acento)])

    def crear_interfaz(self):
        """Crea la interfaz principal"""
        # Cabecera destacada
        header = ttk.Frame(self.root, style='TFrame')
        header.pack(fill=tk.X)
        ttk.Label(header, text="🏗️ Sistema de Cálculo de Costos de Construcción", style='Title.TLabel').pack(pady=18)

        # Frame principal
        main_frame = ttk.Frame(self.root, padding="18 10 18 18", style='TFrame')
        main_frame.pack(fill=tk.BOTH, expand=True)

        # Configurar grid
        main_frame.columnconfigure(0, weight=1, minsize=270)
        main_frame.columnconfigure(1, weight=2)
        main_frame.columnconfigure(2, weight=1, minsize=340)
        main_frame.rowconfigure(0, weight=1)

        # Panel izquierdo - Lista de habitaciones
        self.crear_panel_habitaciones(main_frame)

        # Panel central - Formulario de habitación
        self.crear_panel_formulario(main_frame)

        # Panel derecho - Resumen y controles
        self.crear_panel_resumen(main_frame)

    def crear_panel_habitaciones(self, parent):
        """Crea el panel de lista de habitaciones"""
        frame = ttk.LabelFrame(parent, text="Habitaciones", padding="14", style='TFrame')
        frame.grid(row=0, column=0, sticky="nsew", padx=(0, 18), pady=8)
        frame.columnconfigure(0, weight=1)

        # Lista de habitaciones
        self.lista_habitaciones = tk.Listbox(frame, width=25, height=18, font=('Segoe UI', 11))
        self.lista_habitaciones.pack(fill=tk.BOTH, expand=True, pady=(0, 10))
        self.lista_habitaciones.bind('<<ListboxSelect>>', self.seleccionar_habitacion)

        # Botones
        btn_frame = ttk.Frame(frame, style='TFrame')
        btn_frame.pack(fill=tk.X, pady=(0, 0))
        ttk.Button(btn_frame, text="➕ Nueva Habitación", command=self.nueva_habitacion).pack(fill=tk.X, pady=(0, 7))
        ttk.Button(btn_frame, text="🗑️ Eliminar Habitación", command=self.eliminar_habitacion).pack(fill=tk.X, pady=(0, 7))
        ttk.Button(btn_frame, text="📄 Duplicar Habitación", command=self.duplicar_habitacion).pack(fill=tk.X)

    def crear_panel_formulario(self, parent):
        """Crea el panel del formulario de habitación"""
        frame = ttk.LabelFrame(parent, text="Detalles de Habitación", padding="18", style='TFrame')
        frame.grid(row=0, column=1, sticky="nsew", padx=8, pady=8)
        frame.columnconfigure(1, weight=1)

        # Información básica
        ttk.Label(frame, text="Información Básica", style='Subtitle.TLabel').grid(
            row=0, column=0, columnspan=2, sticky=tk.W, pady=(0, 10))

        # Nombre
        ttk.Label(frame, text="Nombre:", style='Header.TLabel').grid(row=1, column=0, sticky=tk.W, padx=(0, 10))
        self.entry_nombre = ttk.Entry(frame, width=30, font=('Segoe UI', 11))
        self.entry_nombre.grid(row=1, column=1, sticky=(tk.W, tk.E), pady=2)

        # Tipo predefinido
        ttk.Label(frame, text="Tipo:", style='Header.TLabel').grid(row=2, column=0, sticky=tk.W, padx=(0, 10))
        self.combo_tipo = ttk.Combobox(frame, values=listar_tipos_habitacion(), state="readonly", font=('Segoe UI', 11))
        self.combo_tipo.grid(row=2, column=1, sticky=(tk.W, tk.E), pady=2)
        self.combo_tipo.bind('<<ComboboxSelected>>', self.aplicar_tipo_habitacion)

        # Dimensiones
        ttk.Label(frame, text="Dimensiones", style='Subtitle.TLabel').grid(
            row=3, column=0, columnspan=2, sticky=tk.W, pady=(20, 10))

        # Ancho
        ttk.Label(frame, text="Ancho (m):", style='Header.TLabel').grid(row=4, column=0, sticky=tk.W, padx=(0, 10))
        self.entry_ancho = ttk.Entry(frame, width=30, font=('Segoe UI', 11))
        self.entry_ancho.grid(row=4, column=1, sticky=(tk.W, tk.E), pady=2)

        # Largo
        ttk.Label(frame, text="Largo (m):", style='Header.TLabel').grid(row=5, column=0, sticky=tk.W, padx=(0, 10))
        self.entry_largo = ttk.Entry(frame, width=30, font=('Segoe UI', 11))
        self.entry_largo.grid(row=5, column=1, sticky=(tk.W, tk.E), pady=2)

        # Altura
        ttk.Label(frame, text="Altura (m):", style='Header.TLabel').grid(row=6, column=0, sticky=tk.W, padx=(0, 10))
        self.entry_altura = ttk.Entry(frame, width=30, font=('Segoe UI', 11))
        self.entry_altura.grid(row=6, column=1, sticky=(tk.W, tk.E), pady=2)

        # Materiales
        ttk.Label(frame, text="Materiales", style='Subtitle.TLabel').grid(
            row=7, column=0, columnspan=2, sticky=tk.W, pady=(20, 10))

        # Material piso
        ttk.Label(frame, text="Material Piso:", style='Header.TLabel').grid(row=8, column=0, sticky=tk.W, padx=(0, 10))
        self.combo_material_piso = ttk.Combobox(frame, values=listar_nombres_materiales_piso(), 
                                               state="readonly", font=('Segoe UI', 11))
        self.combo_material_piso.grid(row=8, column=1, sticky=(tk.W, tk.E), pady=2)
        self.combo_material_piso.bind('<<ComboboxSelected>>', self.mostrar_precio_material_piso)
        self.entry_precio_piso = ttk.Entry(frame, width=10, font=('Segoe UI', 11))
        self.entry_precio_piso.grid(row=8, column=2, sticky=tk.W, padx=(10, 0))
        self.label_precio_piso = ttk.Label(frame, text="", style='Info.TLabel')
        self.label_precio_piso.grid(row=8, column=3, sticky=tk.W, padx=(10, 0))

        # Material paredes
        ttk.Label(frame, text="Material Paredes:", style='Header.TLabel').grid(row=9, column=0, sticky=tk.W, padx=(0, 10))
        self.combo_material_paredes = ttk.Combobox(frame, values=listar_nombres_materiales_pared(), 
                                                  state="readonly", font=('Segoe UI', 11))
        self.combo_material_paredes.grid(row=9, column=1, sticky=(tk.W, tk.E), pady=2)
        self.combo_material_paredes.bind('<<ComboboxSelected>>', self.mostrar_precio_material_paredes)
        self.entry_precio_paredes = ttk.Entry(frame, width=10, font=('Segoe UI', 11))
        self.entry_precio_paredes.grid(row=9, column=2, sticky=tk.W, padx=(10, 0))
        self.label_precio_paredes = ttk.Label(frame, text="", style='Info.TLabel')
        self.label_precio_paredes.grid(row=9, column=3, sticky=tk.W, padx=(10, 0))

        # Sistema construcción
        ttk.Label(frame, text="Sistema Construcción:", style='Header.TLabel').grid(row=10, column=0, sticky=tk.W, padx=(0, 10))
        self.combo_sistema = ttk.Combobox(frame, values=listar_nombres_sistemas(), state="readonly", font=('Segoe UI', 11))
        self.combo_sistema.grid(row=10, column=1, sticky=(tk.W, tk.E), pady=2)
        self.combo_sistema.bind('<<ComboboxSelected>>', self.mostrar_factor_sistema)
        self.entry_factor_sistema = ttk.Entry(frame, width=10, font=('Segoe UI', 11))
        self.entry_factor_sistema.grid(row=10, column=2, sticky=tk.W, padx=(10, 0))

        # Botones de acción
        btn_frame = ttk.Frame(frame, style='TFrame')
        btn_frame.grid(row=11, column=0, columnspan=2, pady=(20, 0))
        ttk.Button(btn_frame, text="💾 Guardar Cambios", command=self.guardar_habitacion).pack(side=tk.LEFT, padx=(0, 10))
        ttk.Button(btn_frame, text="🧹 Limpiar Formulario", command=self.limpiar_formulario).pack(side=tk.LEFT)

    def crear_panel_resumen(self, parent):
        """Crea el panel de resumen"""
        frame = ttk.LabelFrame(parent, text="Resumen de Proyecto", padding="18", style='TFrame')
        frame.grid(row=0, column=2, sticky="nsew", padx=(18, 0), pady=8)
        frame.columnconfigure(0, weight=1)

        # Nombre del proyecto
        ttk.Label(frame, text="Nombre del Proyecto:", style='Subtitle.TLabel').pack(anchor=tk.W, pady=(0, 5))
        entrada_frame = ttk.Frame(frame, style='TFrame')
        entrada_frame.pack(fill=tk.X, pady=(0, 15))
        self.entry_nombre_casa = ttk.Entry(entrada_frame, font=('Segoe UI', 11))
        self.entry_nombre_casa.pack(side=tk.LEFT, fill=tk.X, expand=True)
        self.entry_nombre_casa.insert(0, self.casa_actual.nombre)
        ttk.Button(entrada_frame, text="Cambiar", command=self.cambiar_nombre_casa).pack(side=tk.RIGHT, padx=(5, 0))

        # Estadísticas generales
        self.label_estadisticas = ttk.Label(frame, text="", style='Info.TLabel', justify=tk.LEFT)
        self.label_estadisticas.pack(anchor=tk.W, pady=(0, 15))

        # Botones principales
        ttk.Button(frame, text="📊 Ver Dashboard", command=self.abrir_dashboard).pack(fill=tk.X, pady=(0, 5))
        ttk.Button(frame, text="📤 Exportar Reporte", command=self.exportar_reporte).pack(fill=tk.X, pady=(0, 5))
        ttk.Button(frame, text="🏠 Nueva Casa", command=self.nueva_casa).pack(fill=tk.X, pady=(0, 5))

        # Detalles de habitación seleccionada
        ttk.Label(frame, text="Habitación Seleccionada:", style='Subtitle.TLabel').pack(anchor=tk.W)
        self.label_detalle_habitacion = ttk.Label(frame, text="", style='Info.TLabel', justify=tk.LEFT)
        self.label_detalle_habitacion.pack(anchor=tk.W, pady=(5, 0))
    
    def seleccionar_casa_al_iniciar(self):
        """Permite seleccionar la casa al iniciar el programa."""
        conn = db.get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT id, nombre FROM casa ORDER BY id DESC")
        casas = cursor.fetchall()
        conn.close()
        if not casas:
            # Si no hay casas, crear una nueva
            self.casa_id = db.guardar_casa("Mi Casa")
            self.casa_actual = Casa("Mi Casa")
            return
        if len(casas) == 1:
            self.casa_id = casas[0][0]
            self.cargar_casa_desde_db(self.casa_id)
            return
        # Si hay varias casas, mostrar selector
        nombres = [c[1] for c in casas]
        seleccion = simpledialog.askstring("Seleccionar Proyecto", f"Proyectos disponibles:\n" + "\n".join(nombres) + "\n\nEscriba el nombre del proyecto a abrir:", initialvalue=nombres[0])
        if seleccion and seleccion in nombres:
            idx = nombres.index(seleccion)
            self.casa_id = casas[idx][0]
            self.cargar_casa_desde_db(self.casa_id)
        else:
            self.casa_id = casas[0][0]
            self.cargar_casa_desde_db(self.casa_id)

    def cargar_casa_desde_db(self, casa_id):
        """Carga la casa y todas sus habitaciones/materiales desde la base de datos."""
        conn = db.get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT nombre FROM casa WHERE id=?", (casa_id,))
        row = cursor.fetchone()
        if not row:
            self.casa_actual = Casa("Mi Casa")
            conn.close()
            return
        self.casa_actual = Casa(row[0])
        self.casa_id = casa_id
        habitaciones_db = db.obtener_habitaciones_por_casa(self.casa_id)
        for h in habitaciones_db:
            habitacion = Habitacion(h[1], h[2], h[3], h[4])
            rel = db.obtener_materiales_habitacion(h[0])
            if rel:
                id_piso, id_paredes, id_sistema = rel
                materiales = db.obtener_materiales()
                for m in materiales:
                    if m[0] == id_piso:
                        habitacion.material_piso = obtener_material_piso(m[1])
                    if m[0] == id_paredes:
                        habitacion.material_paredes = obtener_material_pared(m[1])
                sistemas = db.obtener_sistemas_construccion()
                for s in sistemas:
                    if s[0] == id_sistema:
                        habitacion.sistema_construccion = obtener_sistema_construccion(s[1])
            self.casa_actual.agregar_habitacion(habitacion)
        conn.close()
        # Actualizar nombre en la interfaz
        if hasattr(self, 'entry_nombre_casa'):
            self.entry_nombre_casa.delete(0, tk.END)
            self.entry_nombre_casa.insert(0, self.casa_actual.nombre)

    def cargar_o_crear_casa(self):
        """Carga la casa y habitaciones desde la base de datos, o crea una nueva si no existe."""
        # Intentar cargar la primera casa existente
        conn = db.get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT id, nombre FROM casa ORDER BY id LIMIT 1")
        row = cursor.fetchone()
        if row:
            self.casa_id = row[0]
            self.casa_actual = Casa(row[1])
            # Cargar habitaciones
            habitaciones_db = db.obtener_habitaciones_por_casa(self.casa_id)
            for h in habitaciones_db:
                habitacion = Habitacion(h[1], h[2], h[3], h[4])
                # Cargar materiales y sistema
                rel = db.obtener_materiales_habitacion(h[0])
                if rel:
                    id_piso, id_paredes, id_sistema = rel
                    # Buscar por id en la tabla material/sistema
                    materiales = db.obtener_materiales()
                    for m in materiales:
                        if m[0] == id_piso:
                            habitacion.material_piso = obtener_material_piso(m[1])
                        if m[0] == id_paredes:
                            habitacion.material_paredes = obtener_material_pared(m[1])
                    sistemas = db.obtener_sistemas_construccion()
                    for s in sistemas:
                        if s[0] == id_sistema:
                            habitacion.sistema_construccion = obtener_sistema_construccion(s[1])
                self.casa_actual.agregar_habitacion(habitacion)
        else:
            # Si no hay casas, crear una nueva y guardarla
            self.casa_id = db.guardar_casa("Mi Casa")
            self.casa_actual = Casa("Mi Casa")
        conn.close()

    def nueva_casa(self):
        """Crea una nueva casa y la guarda en la base de datos."""
        respuesta = messagebox.askyesno("Nueva Casa", 
                                       "¿Crear una nueva casa? Se perderán los datos actuales.")
        if respuesta:
            nombre = simpledialog.askstring("Nueva Casa", "Nombre de la nueva casa:", 
                                          initialvalue="Mi Casa")
            if nombre:
                self.casa_id = db.guardar_casa(nombre)
                self.casa_actual = Casa(nombre)
                self.habitacion_seleccionada = None
                self.entry_nombre_casa.delete(0, tk.END)
                self.entry_nombre_casa.insert(0, nombre)
                self.actualizar_lista_habitaciones()
                self.actualizar_resumen()
                self.limpiar_formulario()

    def nueva_habitacion(self):
        """Crea una nueva habitación y la guarda en la base de datos."""
        nombre = simpledialog.askstring("Nueva Habitación", "Nombre de la habitación:")
        if nombre:
            if self.casa_actual.obtener_habitacion(nombre):
                messagebox.showerror("Error", "Ya existe una habitación con ese nombre")
                return
            habitacion = Habitacion(nombre, 3.0, 3.0, 2.5)
            # Guardar en base de datos
            id_hab = db.guardar_habitacion(nombre, 3.0, 3.0, 2.5, self.casa_id)
            # Guardar relación materiales/sistema (vacío por ahora)
            db.guardar_habitacion_material(id_hab, None, None, None)
            self.casa_actual.agregar_habitacion(habitacion)
            self.actualizar_lista_habitaciones()
            self.actualizar_resumen()
            # Seleccionar la nueva habitación
            index = len(self.casa_actual.habitaciones) - 1
            self.lista_habitaciones.selection_set(index)
            self.seleccionar_habitacion(None)

    def eliminar_habitacion(self):
        """Elimina la habitación seleccionada de la base de datos y de la casa."""
        if not self.habitacion_seleccionada:
            messagebox.showwarning("Advertencia", "Seleccione una habitación para eliminar")
            return
        respuesta = messagebox.askyesno("Confirmar", 
                                       f"¿Eliminar la habitación '{self.habitacion_seleccionada.nombre}'?")
        if respuesta:
            # Eliminar de la base de datos
            conn = db.get_db_connection()
            cursor = conn.cursor()
            # Buscar id de la habitacion en la base de datos
            cursor.execute("SELECT id FROM habitacion WHERE nombre = ? AND id_casa = ?", (self.habitacion_seleccionada.nombre, self.casa_id))
            row = cursor.fetchone()
            if row:
                id_hab = row[0]
                cursor.execute("DELETE FROM habitacion_material WHERE id_habitacion = ?", (id_hab,))
                cursor.execute("DELETE FROM habitacion WHERE id = ?", (id_hab,))
                conn.commit()
            conn.close()
            self.casa_actual.eliminar_habitacion(self.habitacion_seleccionada.nombre)
            self.habitacion_seleccionada = None
            self.actualizar_lista_habitaciones()
            self.actualizar_resumen()
            self.limpiar_formulario()

    def guardar_habitacion(self):
        """Guarda los cambios de la habitación y los sincroniza con la base de datos."""
        nombre = self.entry_nombre.get().strip()
        if not nombre:
            messagebox.showerror("Error", "El nombre es obligatorio")
            return
        try:
            ancho = float(self.entry_ancho.get())
            largo = float(self.entry_largo.get())
            altura = float(self.entry_altura.get())
            if ancho <= 0 or largo <= 0 or altura <= 0:
                messagebox.showerror("Error", "Las dimensiones deben ser positivas")
                return
        except ValueError:
            messagebox.showerror("Error", "Las dimensiones deben ser números válidos")
            return
        material_piso = self.combo_material_piso.get()
        precio_piso = self.entry_precio_piso.get()
        if material_piso:
            try:
                precio_piso = float(precio_piso)
            except ValueError:
                precio_piso = 0
        material_paredes = self.combo_material_paredes.get()
        precio_paredes = self.entry_precio_paredes.get()
        if material_paredes:
            try:
                precio_paredes = float(precio_paredes)
            except ValueError:
                precio_paredes = 0
        sistema = self.combo_sistema.get()
        factor_sistema = self.entry_factor_sistema.get()
        if sistema:
            try:
                factor_sistema = float(factor_sistema)
            except ValueError:
                factor_sistema = 1.0
        # Buscar si la habitación ya existe
        habitacion_existente = self.casa_actual.obtener_habitacion(nombre)
        if habitacion_existente:
            # Editar existente
            habitacion = habitacion_existente
            habitacion.ancho = ancho
            habitacion.largo = largo
            habitacion.altura = altura
        else:
            # Crear nueva
            habitacion = Habitacion(nombre, ancho, largo, altura)
            self.casa_actual.agregar_habitacion(habitacion)
        # Asignar materiales y sistema
        if material_piso:
            habitacion.asignar_material_piso(obtener_material_piso(material_piso))
            if habitacion.material_piso:
                habitacion.material_piso.precio_m2 = precio_piso
        if material_paredes:
            habitacion.asignar_material_paredes(obtener_material_pared(material_paredes))
            if habitacion.material_paredes:
                habitacion.material_paredes.precio_m2 = precio_paredes
        if sistema:
            habitacion.asignar_sistema_construccion(obtener_sistema_construccion(sistema))
            if habitacion.sistema_construccion:
                habitacion.sistema_construccion.factor_costo = factor_sistema
        # Guardar en base de datos
        conn = db.get_db_connection()
        cursor = conn.cursor()
        # Buscar id de la habitacion
        cursor.execute("SELECT id FROM habitacion WHERE nombre = ? AND id_casa = ?", (nombre, self.casa_id))
        row = cursor.fetchone()
        if row:
            id_hab = row[0]
            cursor.execute("UPDATE habitacion SET ancho=?, largo=?, altura=? WHERE id=?", (ancho, largo, altura, id_hab))
        else:
            id_hab = db.guardar_habitacion(nombre, ancho, largo, altura, self.casa_id)
        # Buscar o insertar material piso
        id_piso = id_paredes = id_sistema = None
        if material_piso:
            cursor.execute("SELECT id FROM material WHERE nombre=?", (material_piso,))
            r = cursor.fetchone()
            if not r:
                id_piso = db.guardar_material(material_piso, precio_piso, 'piso')
            else:
                id_piso = r[0]
                cursor.execute("UPDATE material SET precio_m2=? WHERE id=?", (precio_piso, id_piso))
        if material_paredes:
            cursor.execute("SELECT id FROM material WHERE nombre=?", (material_paredes,))
            r = cursor.fetchone()
            if not r:
                id_paredes = db.guardar_material(material_paredes, precio_paredes, 'pared')
            else:
                id_paredes = r[0]
                cursor.execute("UPDATE material SET precio_m2=? WHERE id=?", (precio_paredes, id_paredes))
        if sistema:
            cursor.execute("SELECT id FROM sistema_construccion WHERE nombre=?", (sistema,))
            r = cursor.fetchone()
            if not r:
                id_sistema = db.guardar_sistema_construccion(sistema, factor_sistema, habitacion.sistema_construccion.descripcion if habitacion.sistema_construccion else "")
            else:
                id_sistema = r[0]
                cursor.execute("UPDATE sistema_construccion SET factor_costo=? WHERE id=?", (factor_sistema, id_sistema))
        # Actualizar o insertar relación
        cursor.execute("SELECT id FROM habitacion_material WHERE id_habitacion=?", (id_hab,))
        if cursor.fetchone():
            cursor.execute("UPDATE habitacion_material SET id_material_piso=?, id_material_paredes=?, id_sistema_construccion=? WHERE id_habitacion=?", (id_piso, id_paredes, id_sistema, id_hab))
        else:
            db.guardar_habitacion_material(id_hab, id_piso, id_paredes, id_sistema)
        conn.commit()
        conn.close()
        self.actualizar_lista_habitaciones()
        self.actualizar_resumen()
        self.actualizar_detalle_habitacion()
        messagebox.showinfo("Éxito", "Habitación guardada correctamente")
    def duplicar_habitacion(self):
        """Duplica la habitación seleccionada y la guarda en la base de datos."""
        if not self.habitacion_seleccionada:
            messagebox.showwarning("Advertencia", "Seleccione una habitación para duplicar")
            return
        nombre = simpledialog.askstring("Duplicar Habitación", 
                                       "Nombre para la habitación duplicada:",
                                       initialvalue=f"{self.habitacion_seleccionada.nombre} - Copia")
        if nombre:
            if self.casa_actual.obtener_habitacion(nombre):
                messagebox.showerror("Error", "Ya existe una habitación con ese nombre")
                return
            nueva = Habitacion(nombre, 
                             self.habitacion_seleccionada.ancho,
                             self.habitacion_seleccionada.largo,
                             self.habitacion_seleccionada.altura)
            nueva.material_piso = self.habitacion_seleccionada.material_piso
            nueva.material_paredes = self.habitacion_seleccionada.material_paredes
            nueva.sistema_construccion = self.habitacion_seleccionada.sistema_construccion
            # Guardar en base de datos
            id_hab = db.guardar_habitacion(nombre, nueva.ancho, nueva.largo, nueva.altura, self.casa_id)
            # Buscar ids de materiales y sistema
            conn = db.get_db_connection()
            cursor = conn.cursor()
            id_piso = id_paredes = id_sistema = None
            if nueva.material_piso:
                cursor.execute("SELECT id FROM material WHERE nombre=?", (nueva.material_piso.nombre,))
                r = cursor.fetchone()
                if r: id_piso = r[0]
            if nueva.material_paredes:
                cursor.execute("SELECT id FROM material WHERE nombre=?", (nueva.material_paredes.nombre,))
                r = cursor.fetchone()
                if r: id_paredes = r[0]
            if nueva.sistema_construccion:
                cursor.execute("SELECT id FROM sistema_construccion WHERE nombre=?", (nueva.sistema_construccion.nombre,))
                r = cursor.fetchone()
                if r: id_sistema = r[0]
            db.guardar_habitacion_material(id_hab, id_piso, id_paredes, id_sistema)
            conn.close()
            self.casa_actual.agregar_habitacion(nueva)
            self.actualizar_lista_habitaciones()
            self.actualizar_resumen()
    
    def seleccionar_habitacion(self, event):
        """Maneja la selección de habitación"""
        selection = self.lista_habitaciones.curselection()
        if selection:
            index = selection[0]
            self.habitacion_seleccionada = self.casa_actual.habitaciones[index]
            self.cargar_datos_habitacion()
            self.actualizar_detalle_habitacion()
    
    def cargar_datos_habitacion(self):
        """Carga los datos de la habitación seleccionada en el formulario"""
        if not self.habitacion_seleccionada:
            return
        
        h = self.habitacion_seleccionada
        
        # Datos básicos
        self.entry_nombre.delete(0, tk.END)
        self.entry_nombre.insert(0, h.nombre)
        
        self.entry_ancho.delete(0, tk.END)
        self.entry_ancho.insert(0, str(h.ancho))
        
        self.entry_largo.delete(0, tk.END)
        self.entry_largo.insert(0, str(h.largo))
        
        self.entry_altura.delete(0, tk.END)
        self.entry_altura.insert(0, str(h.altura))
        
        # Materiales
        if h.material_piso:
            self.combo_material_piso.set(h.material_piso.nombre)
        else:
            self.combo_material_piso.set("")
        
        if h.material_paredes:
            self.combo_material_paredes.set(h.material_paredes.nombre)
        else:
            self.combo_material_paredes.set("")
        
        if h.sistema_construccion:
            self.combo_sistema.set(h.sistema_construccion.nombre)
        else:
            self.combo_sistema.set("")
    
    def aplicar_tipo_habitacion(self, event):
        """Aplica las dimensiones del tipo de habitación seleccionado"""
        tipo = self.combo_tipo.get()
        if tipo:
            dimensiones = obtener_dimensiones_tipo(tipo)
            
            self.entry_ancho.delete(0, tk.END)
            self.entry_ancho.insert(0, str(dimensiones["ancho"]))
            
            self.entry_largo.delete(0, tk.END)
            self.entry_largo.insert(0, str(dimensiones["largo"]))
            
            self.entry_altura.delete(0, tk.END)
            self.entry_altura.insert(0, str(dimensiones["altura"]))
    
    def limpiar_formulario(self):
        """Limpia el formulario"""
        self.entry_nombre.delete(0, tk.END)
        self.entry_ancho.delete(0, tk.END)
        self.entry_largo.delete(0, tk.END)
        self.entry_altura.delete(0, tk.END)
        self.combo_tipo.set("")
        self.combo_material_piso.set("")
        self.combo_material_paredes.set("")
        self.combo_sistema.set("")
    
    def cambiar_nombre_casa(self):
        """Cambia el nombre de la casa"""
        nuevo_nombre = self.entry_nombre_casa.get().strip()
        if nuevo_nombre:
            self.casa_actual.nombre = nuevo_nombre
            self.actualizar_resumen()
            messagebox.showinfo("Éxito", "Nombre de proyecto actualizado")
    
    def abrir_dashboard(self):
        """Abre el dashboard de gráficos"""
        if not self.casa_actual.habitaciones:
            messagebox.showwarning("Advertencia", "Agregue al menos una habitación para ver el dashboard")
            return
        
        try:
            from graficos import Dashboard
            dashboard = Dashboard(self.casa_actual)
            dashboard.mostrar()
        except ImportError:
            messagebox.showerror("Error", "No se pudo cargar el módulo de gráficos")
    
    def exportar_reporte(self):
        """Exporta un reporte del proyecto"""
        messagebox.showinfo("Funcionalidad", "Función de exportar reporte en desarrollo")
    
    def mostrar_precio_material_piso(self, event=None):
        nombre = self.combo_material_piso.get()
        material = obtener_material_piso(nombre)
        if hasattr(self, 'label_precio_piso'):
            if material:
                self.label_precio_piso.config(text=f"{material.precio_m2:,.0f} $/m²")
                self.entry_precio_piso.delete(0, tk.END)
                self.entry_precio_piso.insert(0, str(material.precio_m2))
            else:
                self.label_precio_piso.config(text="")
                self.entry_precio_piso.delete(0, tk.END)

    def mostrar_precio_material_paredes(self, event=None):
        nombre = self.combo_material_paredes.get()
        material = obtener_material_pared(nombre)
        if hasattr(self, 'label_precio_paredes'):
            if material:
                self.label_precio_paredes.config(text=f"{material.precio_m2:,.0f} $/m²")
                self.entry_precio_paredes.delete(0, tk.END)
                self.entry_precio_paredes.insert(0, str(material.precio_m2))
            else:
                self.label_precio_paredes.config(text="")
                self.entry_precio_paredes.delete(0, tk.END)

    def mostrar_factor_sistema(self, event=None):
        nombre = self.combo_sistema.get()
        sistema = obtener_sistema_construccion(nombre)
        if hasattr(self, 'entry_factor_sistema'):
            if sistema:
                self.entry_factor_sistema.delete(0, tk.END)
                self.entry_factor_sistema.insert(0, str(sistema.factor_costo))
            else:
                self.entry_factor_sistema.delete(0, tk.END)
    
    def actualizar_lista_habitaciones(self):
        """Actualiza la lista de habitaciones en la interfaz"""
        if hasattr(self, 'lista_habitaciones'):
            self.lista_habitaciones.delete(0, 'end')
            for habitacion in self.casa_actual.habitaciones:
                self.lista_habitaciones.insert('end', str(habitacion))

    def actualizar_resumen(self):
        """Actualiza el resumen del proyecto en la interfaz"""
        if hasattr(self, 'label_estadisticas'):
            stats = self.casa_actual.obtener_estadisticas() if hasattr(self.casa_actual, 'obtener_estadisticas') else {}
            texto = f"Habitaciones: {stats.get('cantidad_habitaciones', 0)}\nÁrea Total: {stats.get('area_total', 0):.1f} m²\nVolumen Total: {stats.get('volumen_total', 0):.1f} m³\nCosto Total: {formatear_precio(stats.get('costo_total', 0))}\nCosto por m²: {formatear_precio(stats.get('costo_por_m2', 0))}"
            self.label_estadisticas.config(text=texto)

    def ejecutar(self):
        """Ejecuta la interfaz"""
        self.root.mainloop()


# Función principal para ejecutar la interfaz
def main():
    app = InterfazPrincipal()
    app.ejecutar()

if __name__ == "__main__":
    main()