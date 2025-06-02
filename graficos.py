"""
Dashboard de Visualización para Análisis de Costos de Pintura
Módulo: graficos.py
Autor: Sistema de Análisis de Pintura
Versión: 1.0
"""

import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.gridspec import GridSpec
import numpy as np
import seaborn as sns
from typing import List, Dict, Tuple, Optional
import pandas as pd
from datetime import datetime

# Configuración de estilo
plt.style.use('seaborn-v0_8')
sns.set_palette("husl")

class DashboardPintura:
    """
    Clase principal para generar el dashboard de visualización
    de análisis de costos de pintura
    """
    
    def __init__(self, datos_habitaciones: List[Dict], datos_materiales: Dict):
        """
        Inicializa el dashboard con los datos de habitaciones y materiales
        
        Args:
            datos_habitaciones: Lista de diccionarios con datos por habitación
            datos_materiales: Diccionario con información de materiales
        """
        self.datos_habitaciones = datos_habitaciones
        self.datos_materiales = datos_materiales
        self.colores = ['#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4', '#FFEAA7', 
                       '#DDA0DD', '#98D8C8', '#F7DC6F', '#BB8FCE', '#85C1E9']
    
    def calcular_metricas_generales(self) -> Dict:
        """Calcula métricas generales del proyecto"""
        total_area = sum(hab['area_paredes'] for hab in self.datos_habitaciones)
        total_volumen = sum(hab['volumen'] for hab in self.datos_habitaciones)
        total_costo = sum(hab['costo_total'] for hab in self.datos_habitaciones)
        total_pintura = sum(hab['litros_pintura'] for hab in self.datos_habitaciones)
        
        return {
            'total_area': total_area,
            'total_volumen': total_volumen,
            'total_costo': total_costo,
            'total_pintura': total_pintura,
            'num_habitaciones': len(self.datos_habitaciones),
            'costo_promedio_m2': total_costo / total_area if total_area > 0 else 0
        }
    
    def grafico_barras_habitaciones(self, ax: plt.Axes) -> None:
        """
        Genera gráfico de barras con costos por habitación
        
        Args:
            ax: Eje de matplotlib donde dibujar
        """
        nombres = [hab['nombre'] for hab in self.datos_habitaciones]
        costos = [hab['costo_total'] for hab in self.datos_habitaciones]
        
        barras = ax.bar(nombres, costos, color=self.colores[:len(nombres)], 
                       alpha=0.8, edgecolor='black', linewidth=1)
        
        # Personalización
        ax.set_title('💰 Costo Total por Habitación', fontsize=14, fontweight='bold', pad=20)
        ax.set_xlabel('Habitaciones', fontweight='bold')
        ax.set_ylabel('Costo Total ($)', fontweight='bold')
        ax.tick_params(axis='x', rotation=45)
        
        # Agregar valores sobre las barras
        for barra, costo in zip(barras, costos):
            altura = barra.get_height()
            ax.text(barra.get_x() + barra.get_width()/2., altura + max(costos)*0.01,
                   f'${costo:,.0f}', ha='center', va='bottom', fontweight='bold')
        
        # Línea de promedio
        promedio = np.mean(costos)
        ax.axhline(y=promedio, color='red', linestyle='--', alpha=0.7, 
                  label=f'Promedio: ${promedio:,.0f}')
        ax.legend()
        
        # Grid para mejor lectura
        ax.grid(True, alpha=0.3, axis='y')
    
    def grafico_circular_distribucion(self, ax: plt.Axes) -> None:
        """
        Genera gráfico circular de distribución de costos
        
        Args:
            ax: Eje de matplotlib donde dibujar
        """
        nombres = [hab['nombre'] for hab in self.datos_habitaciones]
        costos = [hab['costo_total'] for hab in self.datos_habitaciones]
        
        # Crear el gráfico circular
        wedges, texts, autotexts = ax.pie(costos, labels=nombres, autopct='%1.1f%%',
                                         colors=self.colores[:len(nombres)],
                                         startangle=90, explode=[0.05]*len(nombres))
        
        # Personalización del texto
        for autotext in autotexts:
            autotext.set_color('white')
            autotext.set_fontweight('bold')
            autotext.set_fontsize(10)
        
        for text in texts:
            text.set_fontweight('bold')
        
        ax.set_title('🥧 Distribución de Costos por Habitación', 
                    fontsize=14, fontweight='bold', pad=20)
    
    def grafico_comparativa_materiales(self, ax: plt.Axes) -> None:
        """
        Genera gráfico comparativo de materiales por habitación
        
        Args:
            ax: Eje de matplotlib donde dibujar
        """
        nombres = [hab['nombre'] for hab in self.datos_habitaciones]
        
        # Separar costos por tipo de material
        costos_pintura = [hab['costo_pintura'] for hab in self.datos_habitaciones]
        costos_primer = [hab['costo_primer'] for hab in self.datos_habitaciones]
        costos_accesorios = [hab['costo_accesorios'] for hab in self.datos_habitaciones]
        
        x = np.arange(len(nombres))
        width = 0.25
        
        # Crear barras agrupadas
        ax.bar(x - width, costos_pintura, width, label='Pintura', 
               color=self.colores[0], alpha=0.8)
        ax.bar(x, costos_primer, width, label='Primer', 
               color=self.colores[1], alpha=0.8)
        ax.bar(x + width, costos_accesorios, width, label='Accesorios', 
               color=self.colores[2], alpha=0.8)
        
        # Personalización
        ax.set_title('🎨 Comparativa de Materiales por Habitación', 
                    fontsize=14, fontweight='bold', pad=20)
        ax.set_xlabel('Habitaciones', fontweight='bold')
        ax.set_ylabel('Costo ($)', fontweight='bold')
        ax.set_xticks(x)
        ax.set_xticklabels(nombres, rotation=45)
        ax.legend()
        ax.grid(True, alpha=0.3, axis='y')
    
    def grafico_areas_volumenes(self, ax: plt.Axes) -> None:
        """
        Genera gráfico de dispersión área vs volumen con tamaño por costo
        
        Args:
            ax: Eje de matplotlib donde dibujar
        """
        areas = [hab['area_paredes'] for hab in self.datos_habitaciones]
        volumenes = [hab['volumen'] for hab in self.datos_habitaciones]
        costos = [hab['costo_total'] for hab in self.datos_habitaciones]
        nombres = [hab['nombre'] for hab in self.datos_habitaciones]
        
        # Normalizar tamaños para el scatter
        tamaños = [(costo/max(costos)) * 500 + 50 for costo in costos]
        
        scatter = ax.scatter(areas, volumenes, s=tamaños, c=costos, 
                           cmap='viridis', alpha=0.7, edgecolors='black')
        
        # Agregar etiquetas
        for i, nombre in enumerate(nombres):
            ax.annotate(nombre, (areas[i], volumenes[i]), 
                       xytext=(5, 5), textcoords='offset points',
                       fontsize=9, fontweight='bold')
        
        # Personalización
        ax.set_title('📐 Análisis Área vs Volumen (Tamaño = Costo)', 
                    fontsize=14, fontweight='bold', pad=20)
        ax.set_xlabel('Área de Paredes (m²)', fontweight='bold')
        ax.set_ylabel('Volumen (m³)', fontweight='bold')
        
        # Colorbar
        cbar = plt.colorbar(scatter, ax=ax)
        cbar.set_label('Costo Total ($)', fontweight='bold')
        
        ax.grid(True, alpha=0.3)
    
    def crear_info_box(self, ax: plt.Axes) -> None:
        """
        Crea una caja de información con métricas clave
        
        Args:
            ax: Eje de matplotlib donde dibujar
        """
        metricas = self.calcular_metricas_generales()
        
        # Ocultar ejes
        ax.set_xlim(0, 10)
        ax.set_ylim(0, 10)
        ax.axis('off')
        
        # Crear caja de información
        info_box = patches.FancyBboxPatch((0.5, 1), 9, 8,
                                         boxstyle="round,pad=0.3",
                                         facecolor='lightblue',
                                         edgecolor='navy',
                                         alpha=0.8)
        ax.add_patch(info_box)
        
        # Texto de información
        info_text = f"""
📊 RESUMEN DEL PROYECTO

🏠 Habitaciones: {metricas['num_habitaciones']}
📏 Área Total: {metricas['total_area']:.1f} m²
📦 Volumen Total: {metricas['total_volumen']:.1f} m³
🎨 Pintura Total: {metricas['total_pintura']:.1f} L

💰 Costo Total: ${metricas['total_costo']:,.0f}
💵 Costo/m²: ${metricas['costo_promedio_m2']:.0f}

📅 Generado: {datetime.now().strftime('%d/%m/%Y %H:%M')}
        """
        
        ax.text(5, 5, info_text, ha='center', va='center',
               fontsize=11, fontweight='bold',
               bbox=dict(boxstyle="round,pad=0.5", facecolor='white', alpha=0.9))
    
    def generar_dashboard_completo(self, figsize: Tuple[int, int] = (20, 12)) -> plt.Figure:
        """
        Genera el dashboard completo con todos los gráficos
        
        Args:
            figsize: Tamaño de la figura (ancho, alto)
            
        Returns:
            Figura de matplotlib con el dashboard
        """
        # Crear figura con grid personalizado
        fig = plt.figure(figsize=figsize)
        gs = GridSpec(3, 3, figure=fig, hspace=0.3, wspace=0.3)
        
        # Título principal
        fig.suptitle('🏠 DASHBOARD DE ANÁLISIS DE COSTOS DE PINTURA 🎨', 
                    fontsize=20, fontweight='bold', y=0.98)
        
        # Gráfico de barras (arriba izquierda)
        ax1 = fig.add_subplot(gs[0, :2])
        self.grafico_barras_habitaciones(ax1)
        
        # Caja de información (arriba derecha)
        ax2 = fig.add_subplot(gs[0, 2])
        self.crear_info_box(ax2)
        
        # Gráfico circular (medio izquierda)
        ax3 = fig.add_subplot(gs[1, 0])
        self.grafico_circular_distribucion(ax3)
        
        # Comparativa de materiales (medio centro-derecha)
        ax4 = fig.add_subplot(gs[1, 1:])
        self.grafico_comparativa_materiales(ax4)
        
        # Análisis de áreas y volúmenes (abajo)
        ax5 = fig.add_subplot(gs[2, :])
        self.grafico_areas_volumenes(ax5)
        
        # Ajustar layout
        plt.tight_layout()
        
        return fig
    
    def guardar_dashboard(self, nombre_archivo: str = "dashboard_pintura.png", 
                         dpi: int = 300) -> None:
        """
        Guarda el dashboard como imagen
        
        Args:
            nombre_archivo: Nombre del archivo a guardar
            dpi: Resolución de la imagen
        """
        fig = self.generar_dashboard_completo()
        fig.savefig(nombre_archivo, dpi=dpi, bbox_inches='tight', 
                   facecolor='white', edgecolor='none')
        plt.show()
        print(f"✅ Dashboard guardado como: {nombre_archivo}")
    
    def mostrar_dashboard(self) -> None:
        """Muestra el dashboard en pantalla"""
        fig = self.generar_dashboard_completo()
        plt.show()


class GraficosIndividuales:
    """
    Clase para generar gráficos individuales específicos
    """
    
    def __init__(self, datos_habitaciones: List[Dict]):
        self.datos_habitaciones = datos_habitaciones
        self.colores = plt.cm.Set3(np.linspace(0, 1, len(datos_habitaciones)))
    
    def grafico_eficiencia_pintura(self) -> plt.Figure:
        """
        Gráfico de eficiencia: litros de pintura por m²
        
        Returns:
            Figura de matplotlib
        """
        fig, ax = plt.subplots(figsize=(12, 6))
        
        nombres = [hab['nombre'] for hab in self.datos_habitaciones]
        eficiencia = [hab['litros_pintura']/hab['area_paredes'] 
                     for hab in self.datos_habitaciones]
        
        barras = ax.bar(nombres, eficiencia, color=self.colores, alpha=0.8)
        
        # Línea de referencia (rendimiento estándar: 0.2 L/m²)
        ax.axhline(y=0.2, color='red', linestyle='--', 
                  label='Rendimiento Estándar (0.2 L/m²)')
        
        ax.set_title('⚡ Eficiencia de Pintura por Habitación', 
                    fontsize=14, fontweight='bold')
        ax.set_ylabel('Litros por m²')
        ax.set_xlabel('Habitaciones')
        ax.tick_params(axis='x', rotation=45)
        ax.legend()
        ax.grid(True, alpha=0.3)
        
        # Agregar valores
        for barra, valor in zip(barras, eficiencia):
            ax.text(barra.get_x() + barra.get_width()/2., 
                   barra.get_height() + 0.005,
                   f'{valor:.3f}', ha='center', va='bottom')
        
        plt.tight_layout()
        return fig
    
    def grafico_costo_beneficio(self) -> plt.Figure:
        """
        Análisis costo-beneficio por m² vs área
        
        Returns:
            Figura de matplotlib
        """
        fig, ax = plt.subplots(figsize=(10, 8))
        
        areas = [hab['area_paredes'] for hab in self.datos_habitaciones]
        costo_m2 = [hab['costo_total']/hab['area_paredes'] 
                    for hab in self.datos_habitaciones]
        nombres = [hab['nombre'] for hab in self.datos_habitaciones]
        
        scatter = ax.scatter(areas, costo_m2, s=200, c=self.colores, 
                           alpha=0.7, edgecolors='black')
        
        # Agregar etiquetas
        for i, nombre in enumerate(nombres):
            ax.annotate(nombre, (areas[i], costo_m2[i]),
                       xytext=(10, 10), textcoords='offset points')
        
        # Línea de tendencia
        z = np.polyfit(areas, costo_m2, 1)
        p = np.poly1d(z)
        ax.plot(areas, p(areas), "r--", alpha=0.8, 
               label=f'Tendencia: y={z[0]:.2f}x+{z[1]:.2f}')
        
        ax.set_title('💹 Análisis Costo-Beneficio: Costo/m² vs Área', 
                    fontsize=14, fontweight='bold')
        ax.set_xlabel('Área de Paredes (m²)')
        ax.set_ylabel('Costo por m² ($)')
        ax.legend()
        ax.grid(True, alpha=0.3)
        
        plt.tight_layout()
        return fig


# NUEVO: Dashboard unificado para Casa
class Dashboard:
    """Dashboard visual para una instancia de Casa"""
    def __init__(self, casa):
        self.casa = casa
        self.colores = [
            '#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4', '#FFEAA7',
            '#DDA0DD', '#98D8C8', '#F7DC6F', '#BB8FCE', '#85C1E9'
        ]

    def mostrar(self):
        import matplotlib.pyplot as plt
        import numpy as np
        from matplotlib.gridspec import GridSpec
        resumen = self.casa.obtener_resumen_completo()
        habitaciones = resumen['habitaciones']
        if not habitaciones:
            print('No hay habitaciones para mostrar en el dashboard.')
            return
        fig = plt.figure(figsize=(18, 10))
        gs = GridSpec(2, 2, figure=fig, hspace=0.3, wspace=0.3)
        # Gráfico de barras de costos
        ax1 = fig.add_subplot(gs[0, 0])
        nombres = [h['nombre'] for h in habitaciones]
        costos = [h['costo_total'] for h in habitaciones]
        ax1.bar(nombres, costos, color=self.colores[:len(nombres)], alpha=0.8, edgecolor='black')
        ax1.set_title('Costo Total por Habitación')
        ax1.set_ylabel('Costo ($)')
        ax1.tick_params(axis='x', rotation=45)
        # Gráfico de áreas
        ax2 = fig.add_subplot(gs[0, 1])
        areas = [h['area_piso'] for h in habitaciones]
        ax2.pie(areas, labels=nombres, autopct='%1.1f%%', colors=self.colores[:len(nombres)])
        ax2.set_title('Distribución de Áreas de Piso')
        # Gráfico de materiales (paredes)
        ax3 = fig.add_subplot(gs[1, 0])
        materiales = [h['material_paredes'] for h in habitaciones]
        unique_mat = list(set(materiales))
        counts = [materiales.count(m) for m in unique_mat]
        ax3.bar(unique_mat, counts, color=self.colores[:len(unique_mat)])
        ax3.set_title('Materiales de Paredes Usados')
        # Resumen general
        ax4 = fig.add_subplot(gs[1, 1])
        ax4.axis('off')
        stats = resumen['estadisticas']
        texto = f"""Habitaciones: {stats['cantidad_habitaciones']}\nÁrea Total: {stats['area_total']:.1f} m²\nVolumen Total: {stats['volumen_total']:.1f} m³\nCosto Total: ${stats['costo_total']:,.0f}\nCosto por m²: ${stats['costo_por_m2']:,.0f}\nMás cara: {stats['habitacion_mas_cara']}\nMás grande: {stats['habitacion_mas_grande']}"""
        ax4.text(0.5, 0.5, texto, ha='center', va='center', fontsize=13, bbox=dict(boxstyle='round', facecolor='white', alpha=0.8))
        fig.suptitle(f'Dashboard de Costos - {self.casa.nombre}', fontsize=18, fontweight='bold')
        plt.tight_layout()
        plt.show()
# Función utilitaria para uso rápido
def crear_dashboard_rapido(datos_habitaciones: List[Dict], 
                          datos_materiales: Dict,
                          mostrar: bool = True,
                          guardar: bool = False,
                          nombre_archivo: str = "dashboard_pintura.png") -> None:
    """
    Función de conveniencia para crear dashboard rápidamente
    
    Args:
        datos_habitaciones: Lista de datos por habitación
        datos_materiales: Diccionario de materiales
        mostrar: Si mostrar el dashboard
        guardar: Si guardar el dashboard
        nombre_archivo: Nombre del archivo si se guarda
    """
    dashboard = DashboardPintura(datos_habitaciones, datos_materiales)
    
    if mostrar:
        dashboard.mostrar_dashboard()
    
    if guardar:
        dashboard.guardar_dashboard(nombre_archivo)


if __name__ == "__main__":
    # Ejemplo de uso del módulo
    print("🎨 Módulo de Gráficos para Análisis de Pintura")
    print("=" * 50)
    print("Funcionalidades disponibles:")
    print("• DashboardPintura: Clase principal para dashboard completo")
    print("• GraficosIndividuales: Gráficos específicos adicionales")
    print("• crear_dashboard_rapido(): Función de conveniencia")
    print("\n¡Listo para visualizar datos de pintura! 📊")