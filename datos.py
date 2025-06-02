"""
Sistema de Cálculo de Costos de Construcción
Archivo: datos.py
Base de datos de materiales, precios y configuraciones
"""

from clases import Material, SistemaConstruccion

# =============================================================================
# MATERIALES PARA PISOS
# =============================================================================

MATERIALES_PISO = {
    "Cerámica Básica": Material("Cerámica Básica", 45000, "piso"),
    "Cerámica Premium": Material("Cerámica Premium", 85000, "piso"),
    "Porcelanato Básico": Material("Porcelanato Básico", 95000, "piso"),
    "Porcelanato Premium": Material("Porcelanato Premium", 150000, "piso"),
    "Porcelanato Rectificado": Material("Porcelanato Rectificado", 180000, "piso"),
    "Madera Laminada": Material("Madera Laminada", 95000, "piso"),
    "Madera Ingeniería": Material("Madera Ingeniería", 140000, "piso"),
    "Madera Natural": Material("Madera Natural", 220000, "piso"),
    "Vinilo SPC": Material("Vinilo SPC", 65000, "piso"),
    "Vinilo Premium": Material("Vinilo Premium", 85000, "piso"),
    "Alfombra Básica": Material("Alfombra Básica", 35000, "piso"),
    "Alfombra Premium": Material("Alfombra Premium", 75000, "piso"),
    "Concreto Pulido": Material("Concreto Pulido", 55000, "piso"),
    "Microcemento": Material("Microcemento", 120000, "piso"),
    "Mármol": Material("Mármol", 280000, "piso"),
    "Granito": Material("Granito", 320000, "piso"),
}

# =============================================================================
# MATERIALES PARA PAREDES
# =============================================================================

MATERIALES_PARED = {
    "Pintura Básica": Material("Pintura Básica", 15000, "pared"),
    "Pintura Premium": Material("Pintura Premium", 25000, "pared"),
    "Pintura Texturizada": Material("Pintura Texturizada", 35000, "pared"),
    "Papel Tapiz Básico": Material("Papel Tapiz Básico", 35000, "pared"),
    "Papel Tapiz Premium": Material("Papel Tapiz Premium", 65000, "pared"),
    "Papel Tapiz 3D": Material("Papel Tapiz 3D", 95000, "pared"),
    "Estuco Tradicional": Material("Estuco Tradicional", 20000, "pared"),
    "Estuco Veneciano": Material("Estuco Veneciano", 85000, "pared"),
    "Cerámica Pared": Material("Cerámica Pared", 75000, "pared"),
    "Porcelanato Pared": Material("Porcelanato Pared", 120000, "pared"),
    "Piedra Natural": Material("Piedra Natural", 180000, "pared"),
    "Ladrillo Vista": Material("Ladrillo Vista", 95000, "pared"),
    "Madera Decorativa": Material("Madera Decorativa", 150000, "pared"),
    "Panel Acústico": Material("Panel Acústico", 110000, "pared"),
    "Yeso Decorativo": Material("Yeso Decorativo", 45000, "pared"),
}

# =============================================================================
# SISTEMAS DE CONSTRUCCIÓN
# =============================================================================

SISTEMAS_CONSTRUCCION = {
    "Mampostería Tradicional": SistemaConstruccion(
        "Mampostería Tradicional", 
        1.0, 
        "Sistema tradicional con ladrillo tolete y mortero de cemento"
    ),
    "Mampostería Estructural": SistemaConstruccion(
        "Mampostería Estructural", 
        1.15, 
        "Ladrillo estructural con mayor resistencia"
    ),
    "Drywall Básico": SistemaConstruccion(
        "Drywall Básico", 
        0.75, 
        "Sistema liviano con perfiles metálicos y láminas de yeso básicas"
    ),
    "Drywall Premium": SistemaConstruccion(
        "Drywall Premium", 
        0.90, 
        "Sistema con láminas de yeso de mayor espesor y mejor aislamiento"
    ),
    "Sistema Industrializado": SistemaConstruccion(
        "Sistema Industrializado", 
        1.25, 
        "Paneles prefabricados con instalación rápida"
    ),
    "Construcción Ecológica": SistemaConstruccion(
        "Construcción Ecológica", 
        1.40, 
        "Materiales sostenibles: bambú, tierra comprimida, materiales reciclados"
    ),
    "Steel Frame": SistemaConstruccion(
        "Steel Frame", 
        1.30, 
        "Estructura metálica liviana con paneles OSB"
    ),
    "Concreto Reforzado": SistemaConstruccion(
        "Concreto Reforzado", 
        1.50, 
        "Sistema de muros en concreto con alta resistencia sísmica"
    ),
}

# =============================================================================
# TIPOS DE HABITACIONES PREDEFINIDAS
# =============================================================================

TIPOS_HABITACION = {
    "Sala": {"ancho": 4.0, "largo": 5.0, "altura": 2.7},
    "Comedor": {"ancho": 3.5, "largo": 4.0, "altura": 2.7},
    "Cocina": {"ancho": 3.0, "largo": 4.0, "altura": 2.7},
    "Habitación Principal": {"ancho": 4.0, "largo": 4.5, "altura": 2.7},
    "Habitación Secundaria": {"ancho": 3.0, "largo": 3.5, "altura": 2.7},
    "Baño Principal": {"ancho": 2.5, "largo": 3.0, "altura": 2.5},
    "Baño Social": {"ancho": 2.0, "largo": 2.5, "altura": 2.5},
    "Estudio": {"ancho": 3.0, "largo": 3.0, "altura": 2.7},
    "Balcón": {"ancho": 2.0, "largo": 6.0, "altura": 2.4},
    "Terraza": {"ancho": 4.0, "largo": 6.0, "altura": 2.4},
    "Garaje": {"ancho": 3.0, "largo": 6.0, "altura": 2.4},
    "Cuarto de Servicio": {"ancho": 2.0, "largo": 2.5, "altura": 2.5},
    "Closet": {"ancho": 1.5, "largo": 2.0, "altura": 2.5},
    "Despensa": {"ancho": 1.5, "largo": 2.0, "altura": 2.5},
    "Zona de Lavado": {"ancho": 2.0, "largo": 2.5, "altura": 2.5},
}

# =============================================================================
# CONFIGURACIONES DEL SISTEMA
# =============================================================================

CONFIGURACION = {
    "moneda": "COP",
    "simbolo_moneda": "$",
    "unidad_area": "m²",
    "unidad_longitud": "m",
    "factor_iva": 0.19,  # 19% IVA
    "factor_administracion": 0.15,  # 15% administración
    "factor_utilidad": 0.20,  # 20% utilidad
    "precision_decimales": 0,
    "mostrar_miles": True,
}

# =============================================================================
# COLORES PARA GRÁFICOS
# =============================================================================

COLORES_GRAFICOS = {
    "primario": "#2E86AB",
    "secundario": "#A23B72", 
    "terciario": "#F18F01",
    "cuaternario": "#C73E1D",
    "quinario": "#592E83",
    "paleta_pisos": ["#FF6B6B", "#4ECDC4", "#45B7D1", "#96CEB4", "#FECA57"],
    "paleta_paredes": ["#FF9FF3", "#54A0FF", "#5F27CD", "#00D2D3", "#FF9F43"],
    "paleta_habitaciones": ["#FF6B6B", "#4ECDC4", "#45B7D1", "#96CEB4", "#FECA57", 
                           "#FF9FF3", "#54A0FF", "#5F27CD", "#00D2D3", "#FF9F43"],
}

# =============================================================================
# FUNCIONES DE UTILIDAD
# =============================================================================

def obtener_material_piso(nombre):
    """Obtiene un material de piso por nombre"""
    return MATERIALES_PISO.get(nombre)

def obtener_material_pared(nombre):
    """Obtiene un material de pared por nombre"""
    return MATERIALES_PARED.get(nombre)

def obtener_sistema_construccion(nombre):
    """Obtiene un sistema de construcción por nombre"""
    return SISTEMAS_CONSTRUCCION.get(nombre)

def listar_nombres_materiales_piso():
    """Lista todos los nombres de materiales de piso"""
    return list(MATERIALES_PISO.keys())

def listar_nombres_materiales_pared():
    """Lista todos los nombres de materiales de pared"""
    return list(MATERIALES_PARED.keys())

def listar_nombres_sistemas():
    """Lista todos los nombres de sistemas de construcción"""
    return list(SISTEMAS_CONSTRUCCION.keys())

def listar_tipos_habitacion():
    """Lista todos los tipos de habitación predefinidos"""
    return list(TIPOS_HABITACION.keys())

def obtener_dimensiones_tipo(tipo):
    """Obtiene las dimensiones predefinidas para un tipo de habitación"""
    return TIPOS_HABITACION.get(tipo, {"ancho": 3.0, "largo": 3.0, "altura": 2.5})

def formatear_precio(precio):
    """Formatea un precio según la configuración"""
    if CONFIGURACION["mostrar_miles"]:
        return f"{CONFIGURACION['simbolo_moneda']}{precio:,.{CONFIGURACION['precision_decimales']}f}"
    else:
        return f"{CONFIGURACION['simbolo_moneda']}{precio:.{CONFIGURACION['precision_decimales']}f}"

def calcular_precio_con_impuestos(precio_base):
    """Calcula el precio final incluyendo IVA, administración y utilidad"""
    precio_con_iva = precio_base * (1 + CONFIGURACION["factor_iva"])
    precio_con_admin = precio_con_iva * (1 + CONFIGURACION["factor_administracion"])
    precio_final = precio_con_admin * (1 + CONFIGURACION["factor_utilidad"])
    return precio_final

def obtener_estadisticas_materiales():
    """Obtiene estadísticas de los materiales disponibles"""
    precios_piso = [m.precio_m2 for m in MATERIALES_PISO.values()]
    precios_pared = [m.precio_m2 for m in MATERIALES_PARED.values()]
    
    return {
        "total_materiales_piso": len(MATERIALES_PISO),
        "total_materiales_pared": len(MATERIALES_PARED),
        "precio_min_piso": min(precios_piso),
        "precio_max_piso": max(precios_piso),
        "precio_promedio_piso": sum(precios_piso) / len(precios_piso),
        "precio_min_pared": min(precios_pared),
        "precio_max_pared": max(precios_pared),
        "precio_promedio_pared": sum(precios_pared) / len(precios_pared),
    }

# =============================================================================
# DATOS DE EJEMPLO PARA TESTING
# =============================================================================

def crear_casa_ejemplo():
    """Crea una casa de ejemplo para testing"""
    from clases import Casa, Habitacion
    
    casa = Casa("Casa Ejemplo")
    
    # Crear habitaciones de ejemplo
    sala = Habitacion("Sala", 4.0, 5.0, 2.7)
    sala.asignar_material_piso(obtener_material_piso("Porcelanato Básico"))
    sala.asignar_material_paredes(obtener_material_pared("Pintura Premium"))
    sala.asignar_sistema_construccion(obtener_sistema_construccion("Mampostería Tradicional"))
    
    cocina = Habitacion("Cocina", 3.0, 4.0, 2.7)
    cocina.asignar_material_piso(obtener_material_piso("Cerámica Premium"))
    cocina.asignar_material_paredes(obtener_material_pared("Cerámica Pared"))
    cocina.asignar_sistema_construccion(obtener_sistema_construccion("Mampostería Tradicional"))
    
    habitacion_principal = Habitacion("Habitación Principal", 4.0, 4.5, 2.7)
    habitacion_principal.asignar_material_piso(obtener_material_piso("Madera Laminada"))
    habitacion_principal.asignar_material_paredes(obtener_material_pared("Pintura Texturizada"))
    habitacion_principal.asignar_sistema_construccion(obtener_sistema_construccion("Drywall Premium"))
    
    # Agregar habitaciones a la casa
    casa.agregar_habitacion(sala)
    casa.agregar_habitacion(cocina)
    casa.agregar_habitacion(habitacion_principal)
    
    return casa