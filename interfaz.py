"""
Sistema de Cálculo de Costos de Construcción
Archivo: interfaz.py
Interfaz gráfica principal con tkinter
"""

import tkinter as tk
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
        self.root.geometry("1200x800")
        self.root.configure(bg='#f0f0f0')
        
        # Datos principales
        self.casa_actual = Casa("Mi Casa")
        self.habitacion_seleccionada = None
        
        # Configurar estilo
        self.configurar_estilo()
        
        # Crear interfaz
        self.crear_interfaz()
        
        # Actualizar vista inicial
        self.actualizar_lista_habitaciones()
        self.actualizar_resumen()
    
    def configurar_estilo(self):
        """Configura el estilo de la interfaz"""
        style = ttk.Style()
        style.theme_use('clam')
        
        # Configurar colores
        style.configure('Title.TLabel', font=('Arial', 16, 'bold'), foreground='#2E86AB')
        style.configure('Subtitle.TLabel', font=('Arial', 12, 'bold'), foreground='#333333')
        style.configure('Info.TLabel', font=('Arial', 10), foreground='#666666')
        style.configure('Success.TLabel', font=('Arial', 10), foreground='#28a745')
        style.configure('Error.TLabel', font=('Arial', 10), foreground='#dc3545')
    
    def crear_interfaz(self):
        """Crea la interfaz principal"""
        # Frame principal
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configurar grid
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        main_frame.rowconfigure(1, weight=1)
        
        # Título principal
        titulo = ttk.Label(main_frame, text="Sistema de Cálculo de Costos de Construcción", 
                          style='Title.TLabel')
        titulo.grid(row=0, column=0, columnspan=3, pady=(0, 20))
        
        # Panel izquierdo - Lista de habitaciones
        self.crear_panel_habitaciones(main_frame)
        
        # Panel central - Formulario de habitación
        self.crear_panel_formulario(main_frame)
        
        # Panel derecho - Resumen y controles
        self.crear_panel_resumen(main_frame)
    
    def crear_panel_habitaciones(self, parent):
        """Crea el panel de lista de habitaciones"""
        frame = ttk.LabelFrame(parent, text="Habitaciones", padding="10")
        frame.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), padx=(0, 10))
        
        # Lista de habitaciones
        self.lista_habitaciones = tk.Listbox(frame, width=25, height=15)
        self.lista_habitaciones.pack(fill=tk.BOTH, expand=True)
        self.lista_habitaciones.bind('<<ListboxSelect>>', self.seleccionar_habitacion)
        
        # Botones
        btn_frame = ttk.Frame(frame)
        btn_frame.pack(fill=tk.X, pady=(10, 0))
        
        ttk.Button(btn_frame, text="Nueva Habitación", 
                  command=self.nueva_habitacion).pack(fill=tk.X, pady=(0, 5))
        ttk.Button(btn_frame, text="Eliminar Habitación", 
                  command=self.eliminar_habitacion).pack(fill=tk.X, pady=(0, 5))
        ttk.Button(btn_frame, text="Duplicar Habitación", 
                  command=self.duplicar_habitacion).pack(fill=tk.X)
    
    def crear_panel_formulario(self, parent):
        """Crea el panel del formulario de habitación"""
        frame = ttk.LabelFrame(parent, text="Detalles de Habitación", padding="10")
        frame.grid(row=1, column=1, sticky=(tk.W, tk.E, tk.N, tk.S), padx=5)
        frame.columnconfigure(1, weight=1)
        
        # Información básica
        ttk.Label(frame, text="Información Básica", style='Subtitle.TLabel').grid(
            row=0, column=0, columnspan=2, sticky=tk.W, pady=(0, 10))
        
        # Nombre
        ttk.Label(frame, text="Nombre:").grid(row=1, column=0, sticky=tk.W, padx=(0, 10))
        self.entry_nombre = ttk.Entry(frame, width=30)
        self.entry_nombre.grid(row=1, column=1, sticky=(tk.W, tk.E), pady=2)
        
        # Tipo predefinido
        ttk.Label(frame, text="Tipo:").grid(row=2, column=0, sticky=tk.W, padx=(0, 10))
        self.combo_tipo = ttk.Combobox(frame, values=listar_tipos_habitacion(), state="readonly")
        self.combo_tipo.grid(row=2, column=1, sticky=(tk.W, tk.E), pady=2)
        self.combo_tipo.bind('<<ComboboxSelected>>', self.aplicar_tipo_habitacion)
        
        # Dimensiones
        ttk.Label(frame, text="Dimensiones", style='Subtitle.TLabel').grid(
            row=3, column=0, columnspan=2, sticky=tk.W, pady=(20, 10))
        
        # Ancho
        ttk.Label(frame, text="Ancho (m):").grid(row=4, column=0, sticky=tk.W, padx=(0, 10))
        self.entry_ancho = ttk.Entry(frame, width=30)
        self.entry_ancho.grid(row=4, column=1, sticky=(tk.W, tk.E), pady=2)
        
        # Largo
        ttk.Label(frame, text="Largo (m):").grid(row=5, column=0, sticky=tk.W, padx=(0, 10))
        self.entry_largo = ttk.Entry(frame, width=30)
        self.entry_largo.grid(row=5, column=1, sticky=(tk.W, tk.E), pady=2)
        
        # Altura
        ttk.Label(frame, text="Altura (m):").grid(row=6, column=0, sticky=tk.W, padx=(0, 10))
        self.entry_altura = ttk.Entry(frame, width=30)
        self.entry_altura.grid(row=6, column=1, sticky=(tk.W, tk.E), pady=2)
        
        # Materiales
        ttk.Label(frame, text="Materiales", style='Subtitle.TLabel').grid(
            row=7, column=0, columnspan=2, sticky=tk.W, pady=(20, 10))
        
        # Material piso
        ttk.Label(frame, text="Material Piso:").grid(row=8, column=0, sticky=tk.W, padx=(0, 10))
        self.combo_material_piso = ttk.Combobox(frame, values=listar_nombres_materiales_piso(), 
                                               state="readonly")
        self.combo_material_piso.grid(row=8, column=1, sticky=(tk.W, tk.E), pady=2)
        
        # Material paredes
        ttk.Label(frame, text="Material Paredes:").grid(row=9, column=0, sticky=tk.W, padx=(0, 10))
        self.combo_material_paredes = ttk.Combobox(frame, values=listar_nombres_materiales_pared(), 
                                                  state="readonly")
        self.combo_material_paredes.grid(row=9, column=1, sticky=(tk.W, tk.E), pady=2)
        
        # Sistema construcción
        ttk.Label(frame, text="Sistema Construcción:").grid(row=10, column=0, sticky=tk.W, padx=(0, 10))
        self.combo_sistema = ttk.Combobox(frame, values=listar_nombres_sistemas(), state="readonly")
        self.combo_sistema.grid(row=10, column=1, sticky=(tk.W, tk.E), pady=2)
        
        # Botones de acción
        btn_frame = ttk.Frame(frame)
        btn_frame.grid(row=11, column=0, columnspan=2, pady=(20, 0))
        
        ttk.Button(btn_frame, text="Guardar Cambios", 
                  command=self.guardar_habitacion).pack(side=tk.LEFT, padx=(0, 10))
        ttk.Button(btn_frame, text="Limpiar Formulario", 
                  command=self.limpiar_formulario).pack(side=tk.LEFT)
    
    def crear_panel_resumen(self, parent):
        """Crea el panel de resumen"""
        frame = ttk.LabelFrame(parent, text="Resumen de Proyecto", padding="10")
        frame.grid(row=1, column=2, sticky=(tk.W, tk.E, tk.N, tk.S), padx=(10, 0))
        
        # Nombre del proyecto
        ttk.Label(frame, text="Nombre del Proyecto:", style='Subtitle.TLabel').pack(anchor=tk.W)
        
        entrada_frame = ttk.Frame(frame)
        entrada_frame.pack(fill=tk.X, pady=(5, 15))
        
        self.entry_nombre_casa = ttk.Entry(entrada_frame)
        self.entry_nombre_casa.pack(side=tk.LEFT, fill=tk.X, expand=True)
        self.entry_nombre_casa.insert(0, self.casa_actual.nombre)
        
        ttk.Button(entrada_frame, text="Cambiar", 
                  command=self.cambiar_nombre_casa).pack(side=tk.RIGHT, padx=(5, 0))
        
        # Estadísticas generales
        self.label_estadisticas = ttk.Label(frame, text="", style='Info.TLabel', justify=tk.LEFT)
        self.label_estadisticas.pack(anchor=tk.W, pady=(0, 15))
        
        # Botones principales
        ttk.Button(frame, text="Ver Dashboard", 
                  command=self.abrir_dashboard).pack(fill=tk.X, pady=(0, 5))
        ttk.Button(frame, text="Exportar Reporte", 
                  command=self.exportar_reporte).pack(fill=tk.X, pady=(0, 5))
        ttk.Button(frame, text="Nueva Casa", 
                  command=self.nueva_casa).pack(fill=tk.X, pady=(0, 15))
        
        # Detalles de habitación seleccionada
        ttk.Label(frame, text="Habitación Seleccionada:", style='Subtitle.TLabel').pack(anchor=tk.W)
        self.label_detalle_habitacion = ttk.Label(frame, text="", style='Info.TLabel', justify=tk.LEFT)
        self.label_detalle_habitacion.pack(anchor=tk.W, pady=(5, 0))
    
    def nueva_habitacion(self):
        """Crea una nueva habitación"""
        nombre = simpledialog.askstring("Nueva Habitación", "Nombre de la habitación:")
        if nombre:
            if self.casa_actual.obtener_habitacion(nombre):
                messagebox.showerror("Error", "Ya existe una habitación con ese nombre")
                return
            
            habitacion = Habitacion(nombre, 3.0, 3.0, 2.5)
            self.casa_actual.agregar_habitacion(habitacion)
            self.actualizar_lista_habitaciones()
            self.actualizar_resumen()
            
            # Seleccionar la nueva habitación
            index = len(self.casa_actual.habitaciones) - 1
            self.lista_habitaciones.selection_set(index)
            self.seleccionar_habitacion(None)
    
    def eliminar_habitacion(self):
        """Elimina la habitación seleccionada"""
        if not self.habitacion_seleccionada:
            messagebox.showwarning("Advertencia", "Seleccione una habitación para eliminar")
            return
        
        respuesta = messagebox.askyesno("Confirmar", 
                                       f"¿Eliminar la habitación '{self.habitacion_seleccionada.nombre}'?")
        if respuesta:
            self.casa_actual.eliminar_habitacion(self.habitacion_seleccionada.nombre)
            self.habitacion_seleccionada = None
            self.actualizar_lista_habitaciones()
            self.actualizar_resumen()
            self.limpiar_formulario()
    
    def duplicar_habitacion(self):
        """Duplica la habitación seleccionada"""
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
            
            # Crear nueva habitación con los mismos datos
            nueva = Habitacion(nombre, 
                             self.habitacion_seleccionada.ancho,
                             self.habitacion_seleccionada.largo,
                             self.habitacion_seleccionada.altura)
            
            nueva.material_piso = self.habitacion_seleccionada.material_piso
            nueva.material_paredes = self.habitacion_seleccionada.material_paredes
            nueva.sistema_construccion = self.habitacion_seleccionada.sistema_construccion
            
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
    
    def guardar_habitacion(self):
        """Guarda los cambios de la habitación"""
        if not self.habitacion_seleccionada:
            messagebox.showwarning("Advertencia", "Seleccione una habitación para editar")
            return
        
        try:
            # Validar datos
            nombre = self.entry_nombre.get().strip()
            if not nombre:
                messagebox.showerror("Error", "El nombre es obligatorio")
                return
            
            ancho = float(self.entry_ancho.get())
            largo = float(self.entry_largo.get())
            altura = float(self.entry_altura.get())
            
            if ancho <= 0 or largo <= 0 or altura <= 0:
                messagebox.showerror("Error", "Las dimensiones deben ser positivas")
                return
            
            # Actualizar habitación
            self.habitacion_seleccionada.nombre = nombre
            self.habitacion_seleccionada.ancho = ancho
            self.habitacion_seleccionada.largo = largo
            self.habitacion_seleccionada.altura = altura
            
            # Materiales
            material_piso = self.combo_material_piso.get()
            if material_piso:
                self.habitacion_seleccionada.asignar_material_piso(obtener_material_piso(material_piso))
            
            material_paredes = self.combo_material_paredes.get()
            if material_paredes:
                self.habitacion_seleccionada.asignar_material_paredes(obtener_material_pared(material_paredes))
            
            sistema = self.combo_sistema.get()
            if sistema:
                self.habitacion_seleccionada.asignar_sistema_construccion(obtener_sistema_construccion(sistema))
            
            # Actualizar interfaz
            self.actualizar_lista_habitaciones()
            self.actualizar_resumen()
            self.actualizar_detalle_habitacion()
            
            messagebox.showinfo("Éxito", "Habitación guardada correctamente")
            
        except ValueError:
            messagebox.showerror("Error", "Las dimensiones deben ser números válidos")
    
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
    
    def nueva_casa(self):
        """Crea una nueva casa"""
        respuesta = messagebox.askyesno("Nueva Casa", 
                                       "¿Crear una nueva casa? Se perderán los datos actuales.")
        if respuesta:
            nombre = simpledialog.askstring("Nueva Casa", "Nombre de la nueva casa:", 
                                          initialvalue="Mi Casa")
            if nombre:
                self.casa_actual = Casa(nombre)
                self.habitacion_seleccionada = None
                self.entry_nombre_casa.delete(0, tk.END)
                self.entry_nombre_casa.insert(0, nombre)
                self.actualizar_lista_habitaciones()
                self.actualizar_resumen()
                self.limpiar_formulario()
    
    def actualizar_lista_habitaciones(self):
        """Actualiza la lista de habitaciones"""
        self.lista_habitaciones.delete(0, tk.END)
        for habitacion in self.casa_actual.habitaciones:
            self.lista_habitaciones.insert(tk.END, str(habitacion))
    
    def actualizar_resumen(self):
        """Actualiza el resumen del proyecto"""
        stats = self.casa_actual.obtener_estadisticas()
        
        texto = f"""Habitaciones: {stats['cantidad_habitaciones']}
Área Total: {stats['area_total']:.1f} m²
Volumen Total: {stats['volumen_total']:.1f} m³
Costo Total: {formatear_precio(stats['costo_total'])}
Costo por m²: {formatear_precio(stats['costo_por_m2'])}"""
        
        if stats['cantidad_habitaciones'] > 0:
            texto += f"""

Habitación más cara: {stats['habitacion_mas_cara']}
Habitación más grande: {stats['habitacion_mas_grande']}"""
        
        self.label_estadisticas.config(text=texto)
    
    def actualizar_detalle_habitacion(self):
        """Actualiza los detalles de la habitación seleccionada"""
        if not self.habitacion_seleccionada:
            self.label_detalle_habitacion.config(text="Ninguna habitación seleccionada")
            return
        
        resumen = self.habitacion_seleccionada.obtener_resumen()
        
        texto = f"""Nombre: {resumen['nombre']}
Dimensiones: {resumen['dimensiones']}
Área Piso: {resumen['area_piso']:.1f} m²
Área Paredes: {resumen['area_paredes']:.1f} m²
Volumen: {resumen['volumen']:.1f} m³

Material Piso: {resumen['material_piso']}
Material Paredes: {resumen['material_paredes']}
Sistema: {resumen['sistema']}

Costo Piso: {formatear_precio(resumen['costo_piso'])}
Costo Paredes: {formatear_precio(resumen['costo_paredes'])}
Costo Total: {formatear_precio(resumen['costo_total'])}"""
        
        self.label_detalle_habitacion.config(text=texto)
    
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
    
    def ejecutar(self):
        """Ejecuta la interfaz"""
        self.root.mainloop()


# Función principal para ejecutar la interfaz
def main():
    app = InterfazPrincipal()
    app.ejecutar()

if __name__ == "__main__":
    main()