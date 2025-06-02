"""
Sistema de Cálculo de Costos de Construcción
Archivo: clases.py
Contiene todas las clases fundamentales del sistema
"""

class Material:
    """Clase para representar materiales de construcción"""
    
    def __init__(self, nombre, precio_m2, tipo="piso"):
        self.nombre = nombre
        self.precio_m2 = precio_m2  # Precio por metro cuadrado
        self.tipo = tipo  # piso, pared, techo, etc.
    
    def __str__(self):
        return f"{self.nombre} - ${self.precio_m2:,.0f}/m²"
    
    def calcular_costo_area(self, area):
        """Calcula el costo para una área específica"""
        return self.precio_m2 * area


class SistemaConstruccion:
    """Clase para sistemas de construcción (mampostería, drywall, etc.)"""
    
    def __init__(self, nombre, factor_costo=1.0, descripcion=""):
        self.nombre = nombre
        self.factor_costo = factor_costo  # Factor multiplicador del costo base
        self.descripcion = descripcion
    
    def __str__(self):
        return f"{self.nombre} (Factor: {self.factor_costo})"
    
    def aplicar_factor(self, costo_base):
        """Aplica el factor del sistema al costo base"""
        return costo_base * self.factor_costo


class Habitacion:
    """Clase para representar una habitación o espacio"""
    
    def __init__(self, nombre, ancho, largo, altura=2.5):
        self.nombre = nombre
        self.ancho = float(ancho)
        self.largo = float(largo)
        self.altura = float(altura)
        self.material_piso = None
        self.material_paredes = None
        self.sistema_construccion = None
        
    def calcular_area_piso(self):
        """Calcula el área del piso"""
        return self.ancho * self.largo
    
    def calcular_area_paredes(self):
        """Calcula el área total de paredes"""
        perimetro = 2 * (self.ancho + self.largo)
        return perimetro * self.altura
    
    def calcular_volumen(self):
        """Calcula el volumen de la habitación"""
        return self.ancho * self.largo * self.altura
    
    def asignar_material_piso(self, material):
        """Asigna material para el piso"""
        self.material_piso = material
    
    def asignar_material_paredes(self, material):
        """Asigna material para las paredes"""
        self.material_paredes = material
    
    def asignar_sistema_construccion(self, sistema):
        """Asigna sistema de construcción"""
        self.sistema_construccion = sistema
    
    def calcular_costo_piso(self):
        """Calcula el costo del piso"""
        if not self.material_piso:
            return 0
        area = self.calcular_area_piso()
        return self.material_piso.calcular_costo_area(area)
    
    def calcular_costo_paredes(self):
        """Calcula el costo de las paredes"""
        if not self.material_paredes:
            return 0
        area = self.calcular_area_paredes()
        return self.material_paredes.calcular_costo_area(area)
    
    def calcular_costo_total(self):
        """Calcula el costo total de la habitación"""
        costo_base = self.calcular_costo_piso() + self.calcular_costo_paredes()
        
        # Aplicar factor del sistema de construcción si existe
        if self.sistema_construccion:
            costo_base = self.sistema_construccion.aplicar_factor(costo_base)
        
        return costo_base
    
    def obtener_resumen(self):
        """Obtiene un resumen de la habitación"""
        return {
            'nombre': self.nombre,
            'dimensiones': f"{self.ancho}m x {self.largo}m x {self.altura}m",
            'area_piso': self.calcular_area_piso(),
            'area_paredes': self.calcular_area_paredes(),
            'volumen': self.calcular_volumen(),
            'material_piso': str(self.material_piso) if self.material_piso else "No asignado",
            'material_paredes': str(self.material_paredes) if self.material_paredes else "No asignado",
            'sistema': str(self.sistema_construccion) if self.sistema_construccion else "No asignado",
            'costo_piso': self.calcular_costo_piso(),
            'costo_paredes': self.calcular_costo_paredes(),
            'costo_total': self.calcular_costo_total()
        }
    
    def __str__(self):
        return f"{self.nombre} ({self.ancho}x{self.largo}m) - ${self.calcular_costo_total():,.0f}"


class Casa:
    """Clase principal para representar una casa completa"""
    
    def __init__(self, nombre="Mi Casa"):
        self.nombre = nombre
        self.habitaciones = []
        self.fecha_creacion = None
        self.observaciones = ""
    
    def agregar_habitacion(self, habitacion):
        """Agrega una habitación a la casa"""
        self.habitaciones.append(habitacion)
    
    def eliminar_habitacion(self, nombre_habitacion):
        """Elimina una habitación por nombre"""
        self.habitaciones = [h for h in self.habitaciones if h.nombre != nombre_habitacion]
    
    def obtener_habitacion(self, nombre):
        """Obtiene una habitación por nombre"""
        for habitacion in self.habitaciones:
            if habitacion.nombre == nombre:
                return habitacion
        return None
    
    def calcular_area_total(self):
        """Calcula el área total de la casa"""
        return sum(h.calcular_area_piso() for h in self.habitaciones)
    
    def calcular_volumen_total(self):
        """Calcula el volumen total de la casa"""
        return sum(h.calcular_volumen() for h in self.habitaciones)
    
    def calcular_costo_total(self):
        """Calcula el costo total de la casa"""
        return sum(h.calcular_costo_total() for h in self.habitaciones)
    
    def calcular_costo_por_m2(self):
        """Calcula el costo por metro cuadrado"""
        area_total = self.calcular_area_total()
        if area_total == 0:
            return 0
        return self.calcular_costo_total() / area_total
    
    def obtener_estadisticas(self):
        """Obtiene estadísticas generales de la casa"""
        if not self.habitaciones:
            return {
                'cantidad_habitaciones': 0,
                'area_total': 0,
                'volumen_total': 0,
                'costo_total': 0,
                'costo_por_m2': 0,
                'habitacion_mas_cara': None,
                'habitacion_mas_grande': None
            }
        
        # Encontrar habitación más cara y más grande
        habitacion_mas_cara = max(self.habitaciones, key=lambda h: h.calcular_costo_total())
        habitacion_mas_grande = max(self.habitaciones, key=lambda h: h.calcular_area_piso())
        
        return {
            'cantidad_habitaciones': len(self.habitaciones),
            'area_total': self.calcular_area_total(),
            'volumen_total': self.calcular_volumen_total(),
            'costo_total': self.calcular_costo_total(),
            'costo_por_m2': self.calcular_costo_por_m2(),
            'habitacion_mas_cara': habitacion_mas_cara.nombre,
            'habitacion_mas_grande': habitacion_mas_grande.nombre
        }
    
    def obtener_resumen_completo(self):
        """Obtiene un resumen completo de la casa"""
        resumen = {
            'nombre_casa': self.nombre,
            'estadisticas': self.obtener_estadisticas(),
            'habitaciones': [h.obtener_resumen() for h in self.habitaciones]
        }
        return resumen
    
    def listar_habitaciones(self):
        """Lista todas las habitaciones"""
        return [h.nombre for h in self.habitaciones]
    
    def __str__(self):
        stats = self.obtener_estadisticas()
        return f"{self.nombre} - {stats['cantidad_habitaciones']} habitaciones, {stats['area_total']:.1f}m², ${stats['costo_total']:,.0f}"


# Función auxiliar para crear materiales comunes
def crear_materiales_base():
    """Crea una lista de materiales base para el sistema"""
    materiales = [
        Material("Cerámica Básica", 45000, "piso"),
        Material("Cerámica Premium", 85000, "piso"),
        Material("Porcelanato", 120000, "piso"),
        Material("Madera Laminada", 95000, "piso"),
        Material("Madera Natural", 180000, "piso"),
        Material("Pintura Estándar", 15000, "pared"),
        Material("Pintura Premium", 25000, "pared"),
        Material("Papel Tapiz", 35000, "pared"),
        Material("Estuco", 20000, "pared"),
    ]
    return materiales

# Función auxiliar para crear sistemas de construcción
def crear_sistemas_construccion():
    """Crea una lista de sistemas de construcción"""
    sistemas = [
        SistemaConstruccion("Mampostería Tradicional", 1.0, "Sistema tradicional con ladrillo y cemento"),
        SistemaConstruccion("Drywall", 0.8, "Sistema liviano con paneles de yeso"),
        SistemaConstruccion("Sistema Industrializado", 1.2, "Prefabricado con mayor costo inicial"),
        SistemaConstruccion("Construcción Ecológica", 1.4, "Materiales sostenibles y técnicas verdes"),
    ]
    return sistemas